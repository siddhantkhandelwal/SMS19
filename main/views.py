from django.shortcuts import render, redirect, reverse
from main.models import UserProfile, Stock, Transaction, StockPurchased
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json
import re
from django.db.models import F

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
