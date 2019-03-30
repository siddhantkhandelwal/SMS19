from django.contrib import admin
from main.models import Stock, Transaction, UserProfile, NewsPost, StockPurchased, Market


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('uid', 'owner', 'stock', 'units',
                    'cost', 'type', 'date_time',)
    search_fields = ('owner__user__username', 'owner__name', )


class StockPurchasedAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'stock', 'units',)
    search_fields = ('owner__user__username', 'owner__name', )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'balance', 'net_worth')
    search_fields = ('user__username', 'name', )


class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'market', 'stock_name', 'stock_price', 'initial_price',
                    'stock_trend', 'price_rate_change_factor', 'available_no_units', 'date_added', 'is_active',)
    search_fields = ('stock_name', )

    def price_rate_change_factor(self, obj):
        return obj.market.price_rate_change_factor


class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'headline', 'body', 'date_added')


class MarketAdmin(admin.ModelAdmin):
    list_display = ('id', 'market_name', 'exchange_rate',
                    'price_rate_change_factor')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(NewsPost, NewsPostAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(StockPurchased, StockPurchasedAdmin)
admin.site.register(Market, MarketAdmin)
