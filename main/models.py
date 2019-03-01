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


class StockPurchased(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    number_purchased = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.stock.stock_name} - {self.owner.name} - {self.number_purchased}"

    class Meta:
        verbose_name_plural = 'Stocks Purchased'
