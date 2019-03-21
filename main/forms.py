from allauth.account.forms import SignupForm
from django import forms
from .validators import SpecialCharacterValidator

class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=30, label='Username', validators=[SpecialCharacterValidator])
    first_name = forms.CharField(max_length=30, label='First Name', validators=[SpecialCharacterValidator])

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.save()
        return user
