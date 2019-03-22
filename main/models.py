from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    balance = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name} - {self.user.username}'


class Stock(models.Model):
    stock_name = models.CharField(max_length=100, unique=True)
    stock_price = models.PositiveIntegerField(default=0)
    market_type = models.CharField(max_length=10, null=False, choices=(
        ('BSE', 'BSE'), ('NYM', 'NYM')), default='BSE')
    initial_price = models.IntegerField(default=0)
    available_no_units = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.stock_name} - {self.market_type}'


class Transaction(models.Model):
    stock = models.ManyToManyField(Stock)
    owner = models.ManyToManyField(UserProfile)
    units = models.IntegerField(default=0)
    cost = models.PositiveIntegerField(default=0)
    type = models.CharField(
        max_length=4, choices=(('B', 'Buy'), ('S', 'Sell')), default='B')
    date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stock.stock_name} - {self.owner.name} - {self.units}"


class StockPurchased(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    units = models.PositiveIntegerField(default=0)


class NewsPost(models.Model):
    headline = models.CharField(null=False, max_length=1000)
    body = models.TextField(null=False)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.headline}'
