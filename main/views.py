from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from main.models import UserProfile, Stock, Transaction, NewsPost, StockPurchased
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import re
from django.db.models import F
import random
import operator


special_character_regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
CONST_RATE_INCREASE = 0.01


@csrf_exempt
def get_stock_purchased(request, code):
    user_profile = UserProfile.objects.get(user=request.user)
    stocks_purchased = StockPurchased.objects.filter(owner=user_profile)
    list_stocks_purchased = []
    for stock_purchased in stocks_purchased:
        if stock_purchased.stock.market_type == code:
            units = stock_purchased.units
            stock_data = [stock_purchased.stock.pk, stock_purchased.stock.stock_name, stock_purchased.stock.stock_price, units]
            list_stocks_purchased.append(stock_data)
    response = {'stocks_purchased': list_stocks_purchased}
    return JsonResponse(response)


def get_balance(request):
    userprofile = UserProfile.objects.get(user=request.user)
    balance = userprofile.balance
    return JsonResponse({'balance': balance})


@csrf_exempt
def get_news_post(request):
    news_list = []
    for news in NewsPost.objects.all():
        news_data = [news.headline, news.body, news.date_added]
        news_list.append(news_data)
    response = {'news_list': news_list}
    return JsonResponse(response)


def test(request):
    return render(request, 'main/useless.html')


def news(request):
    return render(request, 'main/news.html')


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


@csrf_exempt
@login_required
def game(request):
    return render(request, 'main/game.html')


@csrf_exempt
@login_required
def get_stocks_data(request, code):
    try:
        stocks = Stock.objects.filter(market_type=code)
        stocks_list = []
        for stock in stocks:
            stock_data = [stock.pk, stock.stock_name, stock.stock_price,
                          stock.initial_price, stock.available_no_units, ]
            stocks_list.append(stock_data)
        data = {'stocks_list': stocks_list}
        return JsonResponse(data)
    except:
        return JsonResponse({'message': 'Error in Retrieving Stocks'})



@login_required
def portfolio(request):
    return render(request, 'main/portfolio.html')


@login_required
@csrf_exempt
def buy_stock(request, pk):
    if request.method == 'POST':
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except:
            response_data = {'status': 'error',
                             'message': 'User Does not Exist'}
            return JsonResponse(response_data)
        try:
            pk = int(pk)
            stock_to_buy = Stock.objects.get(pk=pk)
        except:
            response_data = {'status': 'error',
                             'message': 'Invalid Stock PK'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        units = int(request.POST['units'])
        cost = stock_to_buy.stock_price * units
        print(cost)
        if (user_profile.balance < cost or units > stock_to_buy.available_no_units):
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
            transaction_uid = random.randint(1, 10000)
            transaction = Transaction.objects.create(
                uid=transaction_uid, owner=user_profile, stock=stock_to_buy)
            transaction.units = units
            transaction.cost = cost
            transaction.type = 'B'
            transaction.save()
            transaction.refresh_from_db()
            try:
                stock_purchased = StockPurchased.objects.get(
                    owner=user_profile, stock=stock_to_buy)
                stock_purchased.units = F('units') + units
                stock_purchased.save()
                stock_purchased.refresh_from_db()
            except:
                stock_purchased = StockPurchased.objects.create(
                    owner=user_profile, stock=stock_to_buy, units=units)
                stock_purchased.refresh_from_db()

            stock_to_buy.stock_price += CONST_RATE_INCREASE * \
                F('stock_price')*units

            response_data = {'status': 'success',
                             'message': f'Transaction#{transaction.uid}: {user_profile.user.username} has successfully purchased {units} units of {stock_to_buy.stock_name} on {transaction.date_time}'}

        except:
            response_data = {'status': 'error',
                             'message': 'Error in Transaction'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
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
            pk = int(pk)
            stock = Stock.objects.get(pk=pk)
            stock_to_sell = StockPurchased.objects.get(
                stock=stock, owner=user_profile)
        except:
            response_data = {'status': 'error',
                             'message': 'Invalid Stock PK/User does not own any units of given Stock'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        units = int(request.POST['units'])
        cost = stock.stock_price * units

        if (units > stock_to_sell.units):
            response_data = {'status': 'error',
                             'message': 'Insufficient No. of Stocks to Sell'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        try:
            user_profile.balance = F('balance') + cost
            user_profile.save()
            user_profile.refresh_from_db()
            stock.available_no_stocks = F('available_no_stocks') + units
            stock.save()
            stock.refresh_from_db()
            if(stock_to_sell.units == units):
                stock_to_sell.delete()
            else:
                stock_to_sell.units = F('units') - units
                stock_to_sell.save()
                stock_to_sell.refresh_from_db()
            transaction_uid = random.randint(1, 10000)
            transaction = Transaction.objects.create(
                uid=transaction_uid, owner=user_profile, stock=stock)
            transaction.units = units
            transaction.cost = cost
            transaction.type = 'S'
            transaction.save()
            transaction.refresh_from_db()
            stock_to_buy.stock_price -= CONST_RATE_INCREASE * \
                F('stock_price')*units
            response_data = {'status': 'success',
                             'message': f'Transaction#{transaction.uid}: {user_profile.user.username} has successfully sold {units} units of {stock.stock_name} on {transaction.date_time}'}
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
            stock.initial_price = initial_price
            stock.stock_price = initial_price
            stock.market_type = market_type
            stock.available_no_units = available_no_units
            stock.save()
            response_data = {'status': 'success',
                             'message': f'Added {stock.stock_name}, {stock.initial_price}, {stock.available_no_units}'}
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
            last_five_added = NewsPost.objects.all().order_by(
                '-date_added')[:5]
        except:
            last_five_added = ''
        return render(request, 'main/add_newspost.html', {'last_five_added': last_five_added})
    except:
        response_data = {'status': 'error',
                         'message': 'Error in Deleting NewsPost'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required
def leaderboard_data(request):
    lb_data = {}
    for user_profile in UserProfile.objects.all():
        try:
            net_worth = 0
            user_stocks_purchased = StockPurchased.objects.filter(
                owner=user_profile)
            for stock_purchased in user_stocks_purchased:
                net_worth += stock_purchased.stock.stock_price
            net_worth += user_profile.balance
            user_profile.net_worth = net_worth
        except:
            response_data = {'status': 'error',
                             'message': 'Error in Calculating Net Worth'}
            return JsonResponse(response_data)
        lb_data[user_profile.user.username] = user_profile.net_worth
        sorted_lb_data = sorted(
            lb_data.items(), key=operator.itemgetter(1), reverse=True)
    list_user_name = [x[0] for x in sorted_lb_data][:10]
    list_net_worth = [x[1] for x in sorted_lb_data][:10]
    count = len(list_net_worth)
    list_rank = [i for i in range(1, count+1)]
    response_data = {'list_rank': list_rank,
                     'list_user_name': list_user_name,
                     'list_net_worth': list_net_worth,
                     }
    return JsonResponse(response_data)


@login_required
def display_leaderboard(request):
    return render(request, 'main/leaderboard.html')
