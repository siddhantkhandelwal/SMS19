from django.shortcuts import render, redirect
from django.core.mail import send_mail
from main.models import UserProfile
from string import punctuation
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json


def register(request):
    if request.user.is_authenticated:
        return redirect('game')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        name = request.POST.get('name')

        if any(special_character in name for special_character in list(punctuation)):
            reponse_data = {'status': 'error',
                            'message': 'Name cannot contain any special character'}
            return HttpResponse(json.dumps(reponse_data), content_type="application/json")

        user = User.objects.create()
        user.username = username
        user.set_password(password)
        user.email = email
        user.save()

        user_profile = UserProfile.objects.create()
        user_profile.user = user
        user_profile.name = name
        user_profile.save()
        login(request, user)
        return redirect('game')
    else:
        return render(request, 'main/register.html', {})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('game')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
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
    return redirect('login')


def user_forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        users = User.objects.filter(email=email)
        if users is None:
            response_data = {'status': 'error',
                             'message': 'Email Address not Registered'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        for user in users:
            new_password = User.objects.make_random_password()
            email_subject = 'Forgot Password | Stock Market Simulation, APOGEE 2019'
            email_message = f'Your new password for username {user.username} is {new_password}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(email_subject, email_message, email_from, recipient_list)
            user.set_password(new_password)
            user.save()
            response_data = {'status': 'success',
                             'message': 'Please check your email for new password'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return render(request, 'main/user_forgot_password.html', {})


@login_required
def game(request):
    return HttpResponse("Giddy Up!")
