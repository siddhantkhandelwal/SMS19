from django.contrib import admin
from main.models import Stock, StockPurchased, UserProfile


admin.site.register(UserProfile)
admin.site.register(Stock)
admin.site.register(StockPurchased)
