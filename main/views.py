from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from main.models import UserProfile
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import re

special_character_regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')

# This function creates a UserProfile for a Social Account login
def create_UserProfile(request, user):
    if UserProfile.objects.filter(user=user).exists():
        pass
    else :
        new_user = UserProfile(user=user, name = user.get_full_name())
        new_user.save()

def register(request):
    if request.user.is_authenticated:
        return redirect('game')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        name = request.POST.get('name')

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
        user.save()

        user_profile = UserProfile.objects.create(user=user)
        user_profile.name = name
        user_profile.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('game')
    else:
        return render(request, 'main/register.html', {})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('game')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if None in [username, password]:
            reponse_data = {'status': 'error',
                            'message': 'One/more of fields missing'}
            return HttpResponse(json.dumps(reponse_data), content_type="application/json")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('game')
        else:
            response_data = {'status': 'error',
                             'message': 'Invalid Username/Password'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return render(request, 'main/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('game'))


def user_forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except:
            response_data = {'status': 'error',
                             'message': 'Email Address not Registered'}
            return render(request, 'main/user_forgot_password.html', response_data)
        new_password = User.objects.make_random_password()
        email_subject = 'Forgot Password | Stock Market Simulation, APOGEE 2019'
        email_message = f'Your new password for username {user.username} is {new_password}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        try:
            send_mail(email_subject, email_message,
                      email_from, recipient_list)
            user.set_password(new_password)
            user.save()
            response_data = {'status': 'success',
                             'message': 'Email Sent! Please check your email for new password'}
        except:
            response_data = {'status': 'error',
                             'message': 'Email could not be sent. Please Contact Us for furthur help'}
        return render(request, 'main/user_forgot_password.html', response_data)
    else:
        return render(request, 'main/user_forgot_password.html', {})


@login_required
def game(request):
    create_UserProfile(request, request.user)
    return HttpResponse("Giddy Up!")
