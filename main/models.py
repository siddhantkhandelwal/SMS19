from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.FloatField(default=200000)
    net_worth = models.FloatField(default=200000)

    def __str__(self):
        return f'{self.name} - {self.user.username}'


class Market(models.Model):
    market_name = models.CharField(max_length=10, unique=True, null=True)
    exchange_rate = models.FloatField(default=1)
    price_rate_change_factor = models.FloatField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.market_name} - {self.exchange_rate}'


class Stock(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE, null=True)
    stock_name = models.CharField(max_length=100, unique=True)
    stock_price = models.PositiveIntegerField(default=0)
    initial_price = models.IntegerField(default=0)
    stock_trend = models.IntegerField(
        default=0, choices=((1, 1), (-1, -1), (0, 0)))
    available_no_units = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.stock_name} - {self.market.market_name}'


class Transaction(models.Model):
    uid = models.AutoField(primary_key=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    units = models.IntegerField(default=0)
    cost = models.PositiveIntegerField(default=0)
    type = models.CharField(
        max_length=4, choices=(('B', 'Buy'), ('S', 'Sell')), default='B')
    date_time = models.DateTimeField(auto_now=True)


class StockPurchased(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    units = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Stocks Purchased'


class NewsPost(models.Model):
    headline = models.CharField(
        null=False, max_length=1000, default="Insert Headline Here")
    body = models.TextField(null=False)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.headline}'
