from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from main.models import UserProfile, Stock, Transaction, NewsPost
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import re
from django.db.models import F

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
    return render(request, 'main/game.html')


@login_required
def profile(request):
    return render(request, 'main/profile.html')


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
            try:
                stock_purchased = StockPurchased.objects.get(
                    owner=user_profile, stock=stock_to_buy)
                stock_purchased.units = F('units') + units
                stock_purchased.save()
                stock_purchased.refresh_from_db()
            except:
                stock_purchased = StockPurchased.objects.create(
                    owner=user_profile, stock=stock_to_buy, units=units)
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
            response_data = {'status': 'success',
                             'message': f'{user_profile.user.username} has successfully sold {units} units of  {stock.stock_name} on {transaction.date_time}'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except:
            response_data = {'status': 'error',
                             'message': 'Error in Transaction'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def add_stock(request):
    if request.method == 'POST':
        stock_name = request.POST.get('stock_name')
        initial_price = request.POST.get('initial_price')
        market_type = request.POST.get('market_type')
        available_no_units = request.POST.get('available_no_units')
        try:
            stock = Stock.objects.create(stock_name=stock_name)
            stock.inital_price = initial_price
            stock.stock_price = initial_price
            stock.market_type = market_type
            stock.available_no_units = available_no_units
            stock.save()
            response_data = {'status': 'success',
                             'message': f'Added {stock.stock_name}, {stock.inital_price}, {stock.available_no_units}'}
        except:
            try:
                stock.delete()
            except:
                pass
            response_data = {'status': 'error',
                             'message': 'Error in adding Stock'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    try:
        last_five_added = Stock.objects.all().order_by('-date_added')[:5]
    except:
        last_five_added = ''
    return render(request, 'main/add_stock.html', {'last_five_added': last_five_added})


@login_required
def delete_stock(request, pk):
    try:
        stock = Stock.objects.get(pk=pk)
        stock.delete()
        response_data = {'status': 'success',
                         'message': 'Deleted'}
        try:
            last_five_added = Stock.objects.all().order_by('-date_added')[:5]
        except:
            last_five_added = ''
        return render(request, 'main/add_stock.html', {'last_five_added': last_five_added})
    except:
        response_data = {'status': 'error',
                         'message': 'Error in Deleting Stock'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def add_newspost(request):
    if request.method == 'POST':
        headline = request.POST.get('headline')
        body = request.POST.get('body')
        try:
            newspost = NewsPost.objects.create(headline=headline)
            newspost.body = body
            newspost.save()
            response_data = {'status': 'success',
                             'message': f'Added {newspost.headline}'}
        except:
            try:
                newspost.delete()
            except:
                pass
            response_data = {'status': 'error',
                             'message': 'Error in adding NewsPost'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
    try:
        last_five_added = NewsPost.objects.all().order_by('-date_added')[:5]
    except:
        last_five_added = ''
    return render(request, 'main/add_newspost.html', {'last_five_added': last_five_added})


@login_required
def delete_newspost(request, pk):
    try:
        newspost = NewsPost.objects.get(pk=pk)
        newspost.delete()
        response_data = {'status': 'success',
                         'message': 'Deleted'}
        try:
            last_five_added = NewsPost.objects.all().order_by('-date_added')[:5]
        except:
            last_five_added = ''
        return render(request, 'main/add_newspost.html', {'last_five_added': last_five_added})
    except:
        response_data = {'status': 'error',
                         'message': 'Error in Deleting NewsPost'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
