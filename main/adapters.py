from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from main.models import UserProfile
from django.shortcuts import redirect

class SocialAccountAdapter(DefaultSocialAccountAdapter):


    def save_user(self, request, sociallogin, form=None):
        user = DefaultSocialAccountAdapter.save_user(
            self, request, sociallogin, form=form)
        if UserProfile.objects.filter(user=user).exists():
            pass
        else:
            new_user = UserProfile(user=user, name=user.get_full_name())
            new_user.save()
        # print("Inside the adapter")
        return redirect('/')
        
