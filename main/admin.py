from django.contrib import admin
from main.models import Stock, Transaction, UserProfile, NewsPost


admin.site.register(UserProfile)
admin.site.register(Stock)
admin.site.register(NewsPost)
admin.site.register(Transaction)
