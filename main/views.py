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


@csrf_exempt
def get_stock_purchased(request):
    user_profile = UserProfile.objects.get(user=request.user)
    stocks_purchased = StockPurchased.objects.filter(owner=user_profile)
    list_stocks_purchased = []
    for stock_purchased in stocks_purchased:
        units = stock_purchased.units
        price = stock_purchased.stock.stock_price
        total = int(units) * int(price)
        stock_data = [stock_purchased.stock.stock_name, units, price, total]
        list_stocks_purchased.append(stock_data)
    response = {'stocks_purchased': list_stocks_purchased}
    return JsonResponse(response)


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

@login_required
def game(request):
    return render(request, 'main/game.html')


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
def profile(request):
    return render(request, 'main/profile.html')


# @login_required
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
            stock_to_buy = Stock.objects.get(pk=pk)
        except:
            response_data = {'status': 'error',
                             'message': 'Invalid Stock PK'}
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        units = int(request.POST['units'])
        cost = stock_to_buy.stock_price * units
        if (user_profile.balance < cost and units < stock_to_buy.available_no_units):
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
                stock_purchased = StockPurchased.objects.create(
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
