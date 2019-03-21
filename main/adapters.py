from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from main.models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponse
import json
import re


class SocialAccountAdapter(DefaultSocialAccountAdapter):


    def save_user(self, request, sociallogin, form=None):
        user = DefaultSocialAccountAdapter.save_user(
            self, request, sociallogin, form=form)
        if UserProfile.objects.filter(user=user).exists():
            pass
        else:
            new_user = UserProfile(user=user, name=user.get_full_name())
            new_user.save()
        return redirect('/')
        
class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        username = data.get('username')
        password = data.get('password1')
        email = data.get('email')
        name = data.get('first_name')
# The check for presence of all the fields is not needed  & hence removed as these are marked as required in frontend

        user = User.objects.create(username=username)
        user.set_password(password)
        user.email = email
        user_name = name.split()
        user.first_name = user_name[0]
        user.last_name = user_name[-1]
        user.save()

        user_profile = UserProfile.objects.create(user=user)
        user_profile.name = name
        user_profile.save()
        
        return user
