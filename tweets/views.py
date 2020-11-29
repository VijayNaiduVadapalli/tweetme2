import random
from django.conf import settings
from django.http import HttpResponse,Http404,JsonResponse
from django.shortcuts import render,redirect 
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes

from .forms import TweetForm
from .models import Tweet
from .serializers import ( 
   TweetSerializer,
   TweetCreateSerializer,TweetActionSerializer)

def home_view(request,*args,**kwargs):
    return render(request,'pages/home.html',context={},status=200)


@api_view(['POST']) #http method client sends
#@authentication_classes([IsAuthenticated])
@permission_classes([IsAuthenticated])
def tweet_create_view(request,*args,**kwargs):
    serializer=TweetCreateSerializer(data=request.POST or None)
    if serializer.is_valid(raise_exception=True):
       obj=serializer.save(user=request.user)
       return Response(serializer.data,status=201)
    return Response({},status=404)




@api_view(['GET'])
def tweet_list_view(request,*args,**kwargs):
    qs=Tweet.objects.all()
    serializer=TweetSerializer(qs,many=True)
    return Response(serializer.data,status=200)


@api_view(['GET'])
def tweet_detail_view(request,tweet_id,*args,**kwargs):
    qs=Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
       return Response({},status=404)
    serializer=TweetSerializer(obj)
    return Response(serializer.data,status=200)

@api_view(['DELETE','POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request,tweet_id,*args,**kwargs):
    qs=Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
       return Response({},status=404)
    qs=qs.filter(user=request.user)
    if not qs.exists():
       return Response({"message":"you cannot delete"},status=404)
    obj=qs.first()
    obj.delete()
    return Response({"message":"tweet removed"},status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request,*args,**kwargs):
    ''' id is required.
   Action is like , unlike , retweet'''
    serializer=TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
       data=serializer.validated_data
       tweet_id=data.get("id")
       action=data.get("action")
       content=data.get("content")

    qs=Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
       return Response({},status=404)
    obj=qs.first()
    if action=="like":
       obj.likes.add(request.user)
       serializer=TweetSerializer(obj)
       return Response(serializer.data,status=200)
    elif action=="unlike":
       obj.likes.remove(request.user)
       serializer=TweetSerializer(obj)
       return Response(serializer.data,status=200)
    elif action=="retweet":
       new_tweet=Tweet.objects.create(user=request.user,parent=obj,content=content)
       serializer=TweetSerializer(new_tweet)
       return Response(serializer.data,status=200)
    return Response({},status=200)



def tweet_create_view_pure_django(request,*args,**kwargs):
    if not request.user.is_authenticated:
       user=None
       if request.is_ajax():
          return JsonResponse({},status=401)
       return redirect(settings.LOGIN_URL)
    form=TweetForm(request.POST or None)
    print('post data is',request.POST)
    next_url=request.POST.get("next") or None
    print("next_url",next_url)
    if form.is_valid():
       obj=form.save(commit=False)
       obj.user=user
       obj.save()
       if request.is_ajax():
          return JsonResponse(obj.serialize(),status=201)
       if next_url !=None and is_safe_url(next_url, ALLOWED_HOSTS):
          return redirect(next_url)  
       form=TweetForm()
    return render(request,'components/form.html',context={"form":form})

def tweet_list_view_pure_django(request,*args,**kwargs):
    qs=Tweet.objects.all() 
    tweet_list=[x.serialize() for x in qs]
    data={
      "isUser":False,
      "response":tweet_list
      }
    return JsonResponse(data)
def tweet_detail_view_pure_django(request,tweet_id,*args,**kwargs):
      """RestAPI view by javascript returns json data"""
      data={
      "isuser":False,
       "id":tweet_id
      }
      status=200
      try:
         obj=Tweet.objects.get(id=tweet_id)
         data['content']=obj.content
      except:  
         data['message']="Not Found"
         status =404
      return JsonResponse(data,status=status)


