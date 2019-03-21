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

        from allauth.account.utils import user_username, user_email, user_field

        data = form.cleaned_data
        name = data.get('first_name')
        email = data.get('email')
        username = data.get('username')
        user_email(user, email)
        user_username(user, username)
        name_split = name.split()
        if len(name):
            user_field(user, 'first_name', name_split[0])
        if len(name)>1:
            user_field(user, 'last_name', name_split[-1])
        if 'password1' in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()

        user_profile = UserProfile.objects.create(user=user)
        user_profile.name = name
        user_profile.save()
        
        return user
