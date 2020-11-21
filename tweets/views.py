from django.http import HttpResponse,Http404
from django.shortcuts import render

def home_view(request,*args,**kwargs):
     return HttpResponse("<div>hello world </div>")
def tweet_detail_view(request,tweet_id,*args,**kwargs):
     try:
        obj=Tweet.objects.get(id=tweet_id)
     except:
        raise Http404
     return HttpResponse(f"<h1>hello {tweet_id} -{obj.content}</h1>")


