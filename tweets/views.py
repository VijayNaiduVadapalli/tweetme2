import random
from django.conf import settings
from django.http import HttpResponse,Http404,JsonResponse
from django.shortcuts import render,redirect 
from django.utils.http import is_safe_url

from .forms import TweetForm
from .models import Tweet

def home_view(request,*args,**kwargs):
    return render(request,'pages/home.html',context={},status=200)

def tweet_create_view(request,*args,**kwargs):
    form=TweetForm(request.POST or None)
    print('post data is',request.POST)
    next_url=request.POST.get("next") or None
    print("next_url",next_url)
    if form.is_valid():
       obj=form.save(commit=False)
       obj.save()
       if next_url !=None and is_safe_url(next_url,ALLOWED_HOSTS):
          return redirect(next_url)  
       form=TweetForm()
    return render(request,'components/form.html',context={"form":form})

def tweet_list_view(request,*args,**kwargs):
    qs=Tweet.objects.all()
    tweet_list=[{"id":x.id, "content":x.content,"likes":random.randint(0,500)}for x in qs]
    data={
      "response":tweet_list
      }
    return JsonResponse(data)
def tweet_detail_view(request,tweet_id,*args,**kwargs):
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


