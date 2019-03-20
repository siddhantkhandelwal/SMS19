from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from main.models import UserProfile, Stock, Transaction, StockPurchased
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import re
from django.db.models import F
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site

special_character_regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')


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
        user.is_active = False
        user.save()

        user_profile = UserProfile.objects.create(user=user)
        user_profile.name = name
        user_profile.save()
        # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#<----------------------Activation mail code starts------------------------------------------------->
        current_site = get_current_site(request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('main/acc_activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token': account_activation_token.make_token(user),
            'request': request
        })
        email_from = settings.EMAIL_HOST_USER
        send_mail( mail_subject, message, email_from, [ email ])
        return HttpResponse('Please confirm your email address to complete the registration')
    else:
        return render(request, 'main/register.html', {})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        # TODO : add a appropriate flash message and a redirect url
    else:
        return HttpResponse('Activation link is invalid!')

# <----------------------Activation mail  code ends------------------------------------------>
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
        # Just to check if the user has used activated the acount using confirmation mail
        try:
            if not User.objects.filter(username=username).is_active :
                response_data = {'status': 'error',
                                'message': 'Please confirm your account uing confirmation mail sent. '}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except Exception:
                response_data = {'status': 'error',
                        'message': 'No such username'}
                return HttpResponse(json.dumps(response_data), content_type="application/json")
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
    return HttpResponse("Giddy Up!")


@login_required
def buy_stock(request, pk):
    if request.method == 'POST':
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except:
            response_data = {'status': 'error',
                             'message': 'User Does not Exist'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        try:
            stock_to_buy = Stock.objects.get(pk=pk)
        except:
            response_data = {'status': 'error',
                             'message': 'Invalid Stock PK'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        units = request.POST['units']
        cost = stock_to_buy.stock_price * units
        if (user_profile.balance < cost & units < stock_to_buy.available_no_units):
            response_data = {'status': 'error',
                             'message': 'Insufficient Balance for Transaction or Insufficient No. of Stocks to Buy'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        try:
            user_profile.balance = F('balance') - cost
            user_profile.save()
            user_profile.refresh_from_db()
            stock_to_buy.available_no_units = F('available_no_units') - units
            stock_to_buy.save()
            stock_to_buy.refresh_from_db()
            transaction = Transaction.objects.create(
                stock=stock_to_buy, owner=user_profile, units=units, cost=cost, type='B')
            transaction.refresh_from_db()
            response_data = {'status': 'success',
                             'message': f'{user_profile.user.username} has successfully purchased {units} units of  {stock_to_buy.stock_name} on {transaction.date_time}'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except:
            response_data = {'status': 'error',
                             'message': 'Error in Transaction'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def sell_stock(request, pk):
    if request.method == 'POST':
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except:
            response_data = {'status': 'error',
                             'message': 'User Does not Exist'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        try:
            stock = Stock.objects.get(pk=pk)
            stock_to_sell = StockPurchased.objects.get(
                stock=stock, owner=user_profile)
        except:
            response_data = {'status': 'error',
                             'message': 'Invalid Stock PK/User does not own any units of given Stock'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        units = request.POST['units']
        cost = stock_to_sell.stock_price * units

        if (units > stock_to_sell.units):
            response_data = {'status': 'error',
                             'message': 'Insufficient No. of Stocks to Sell'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        try:
            user_profile.balance = F('balance') + cost
            user_profile.save()
            user_profile.refresh_from_db()
            stock = F('available_no_stocks') - units
            stock.save()
            stock.refresh_from_db()
            transaction = Transaction.objects.create(
                stock=stock, owner=user_profile, units=units, cost=cost, type='S')
            transaction.refresh_from_db()
            response_data = {'status': 'success',
                             'message': f'{user_profile.user.username} has successfully sold {units} units of  {stock.stock_name} on {transaction.date_time}'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except:
            response_data = {'status': 'error',
                             'message': 'Error in Transaction'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
