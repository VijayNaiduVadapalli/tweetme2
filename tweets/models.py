import random
from django.conf import settings
from django.db import models

User=settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    tweet=models.ForeignKey("Tweet",on_delete=models.CASCADE)
    time_stamp=models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
     #id=models.AutoField(primary_key=True)
     parent=models.ForeignKey("self",null=True,on_delete=models.SET_NULL)
     user=models.ForeignKey(User,on_delete=models.CASCADE) #many users manmy tweets, deletes when user deletes
     likes=models.ManyToManyField(User,related_name='tweet_user',blank=True,through=TweetLike)
     content=models.TextField(blank=True,null=True)
     image=models.FileField(upload_to='images/', blank=True, null=True)
     time_stamp=models.DateTimeField(auto_now_add=True)


     class Meta:
        ordering=['-id'] 

     @property
     def is_retweet(self):
        return self.parent!=None

  
     def serialize(self):
        return {
              "id":self.id,
              "content":self.content,
              "likes": random.randint(0,200)
          }

