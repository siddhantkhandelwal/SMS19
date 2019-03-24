from django.contrib import admin
from main.models import Stock, Transaction, UserProfile, NewsPost, StockPurchased


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('uid', 'owner', 'stock', 'units',
                    'price_at_transaction', 'cost', 'type', 'date_time',)

    def price_at_transaction(self, obj):
        return obj.cost/obj.units


class StockPurchasedAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'stock', 'units',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'balance',)


class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'stock_name', 'stock_price', 'market_type',
                    'initial_price', 'available_no_units', 'date_added')


class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'headline', 'body', 'date_added')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(NewsPost, NewsPostAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(StockPurchased, StockPurchasedAdmin)
