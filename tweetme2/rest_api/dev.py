from django.contrib.auth import get_user_model
from rest_framework import authentication

User=get_user_model()

class DevAuthentication(authentication.BasicAuthentication):
    def authenticated(self,request):
        qs=User.objects.all()
        user=qs.order_by("?").first()  #random user ? 
        return(user,None)