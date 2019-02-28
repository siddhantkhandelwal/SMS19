from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} - {self.user.username}'


class Stock(models.Model):
    stock_name = models.CharField(max_length=100)
    stock_price = models.IntegerField(default=0)
    market_type = models.CharField(max_length=10, null=False, choices=(
        ('BSE', 'BSE'), ('NYM', 'NYM')), default='BSE')
    initial_price = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.stock_name} - {self.market_type}'
