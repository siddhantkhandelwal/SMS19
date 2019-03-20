from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from main.models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponse
import json
import re

special_character_regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')

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
        if None in [username, password, email, name]:
            reponse_data = {'status': 'error',
                            'message': 'One/more of fields missing'}
            return HttpResponse(json.dumps(reponse_data), content_type="application/json")

        if special_character_regex.search(name) or special_character_regex.search(username):
            reponse_data = {'status': 'error',
                            'message': 'Special characters not allowed'}
            return HttpResponse(json.dumps(reponse_data), content_type="application/json")

        if username in [user.username for user in User.objects.all()]:
            reponse_data = {'status': 'error',
                            'message': 'User with the same username already exists'}
            return HttpResponse(json.dumps(reponse_data), content_type="application/json")
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
