from django.conf import settings
from rest_framework import serializers
from .models import Tweet

MAX_TWEET_LENGTH=settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS=settings.TWEET_ACTION_OPTIONS



class TweetCreateSerializer(serializers.ModelSerializer):
    likes=serializers.SerializerMethodField(read_only=True)
    content=serializers.SerializerMethodField(read_only=True)
    #is_retweet=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=Tweet
        field=['id','content','likes','is_retweet']

    def get_likes(self,obj):
        return obj.likes.count()

    def get_content(self,obj):
        content=obj.content
        if obj.is_retweet:
            content=obj.parent.content
        return content




class TweetActionSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    action=serializers.CharField()
    content=serializers.CharField(allow_blank=True,required=False)

    def validate_action(self,value):
        value=value.lower().strip() #"like"-->"like"
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("this is not valid action ")
        return value


class TweetSerializer(serializers.ModelSerializer):
    likes=serializers.SerializerMethodField(read_only=True)
    parent=TweetCreateSerializer(read_only=True)
    class Meta:
        model=Tweet
        field=['id','content','likes','parent']

    def get_likes(self,obj):
        return obj.likes.count()

    def validate_content(self,value):
        if len(value)>MAX_TWEET_LENGTH:
           raise serializers.ValidationError("this is two long")
        return value





