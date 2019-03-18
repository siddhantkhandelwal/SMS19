from django.contrib import admin
from main.models import Stock, Transaction, UserProfile


admin.site.register(UserProfile)
admin.site.register(Stock)
admin.site.register(Transaction)
