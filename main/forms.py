from allauth.account.forms import SignupForm
from django import forms


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.save()
        return user
