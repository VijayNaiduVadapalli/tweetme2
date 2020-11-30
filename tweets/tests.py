from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient # from restAPI testing module

from .models import Tweet

# Create your tests here.

User=get_user_model()

class TweetTestCase(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='cfe',password='something')
        self.user=User.objects.create_user(username='cfe-2',password='something2')
        Tweet.objects.create(content="my first tweet",user=self.user)
        Tweet.objects.create(content="my first tweet",user=self.user)
        Tweet.objects.create(content="my first tweet",user=self.user)
        self.currentCount=Tweet.objects.all().count()

    def test_user_created(self):
        self.assertEqual(self.user.username,"cfe")
        
    def test_tweet_created(self):
        tweet_obj=Tweet.objects.create(content="my tweet",user=self.user)
        self.assertEqual(tweet_obj.user,self.user)
        self.assertEqual(tweet_obj.id, 1)
    
    def get_client(self):
        client=APIClient()
        client.login(username=self.user.username,password='somepassword')
        return client
    
    def test_tweet_list(self):
        client=self.get_client()
        response=client.get("/api/tweets")
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.json(),1))

    def test_action_like(self):
        client=self.get_client()
        response=client.post("/api/tweets/action/",{"id":1,"action":"like"})
        self.assertEqual(response.status_code,200)
        like_count=response.json().get("likes")
        self.assertEqual(like_count,0)
        print(response.json())
    
    def test_action_retweet(self):
        client=self.get_client()
        current_count=self.currentCount
        response=client.post("/api/tweets/action/",{"id":2,"action":"retweet"})
        self.assertEqual(response.status_code,201)
        data =response.json()
        new_tweet_id=data.get("id")
        self.assertNotEqual(2,new_tweet_id)
        self.assertEqual(current_count+1,new_tweet_id)

    def test_tweet_detail_api_view(self):
        client=self.get_client()
        response=client.get("/api/tweets/1/")
        self.assertEqual(response.status_code,200)
        _id=data.get("id")
        self.assertEqual(_id,1)

    def test_tweet_delete_api_view(self):
        client=self.get_client()
        response=client.delete("/api/tweets/1/delete")
        self.assertEqual(response.status_code,200)
        client=self.get_client()
        response=client.delete("/api/tweets/1/delete")
        self.assertEqual(response.status_code,404)
        response_incorrect_owner=client.delete("/api/tweets/3/delete/")
        self.assertEqual(response_incorrect_owner.status_code,401)
        





