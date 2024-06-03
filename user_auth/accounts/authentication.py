from typing import Any
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http.request import HttpRequest


class LoginAndSignupBackend(BaseBackend):
    """Get username and password and authenticate user """
    def authenticate(self, request, username, password,**kwargs):
        try:
            user=User.objects.get(username=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            user=User(username=username)
            user.set_password(password)
            user.email= kwargs['email']
            user.is_active =False
            user.save()
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
