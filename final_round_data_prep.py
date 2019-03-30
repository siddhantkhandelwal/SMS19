from django.conf import settings
import os


def clean():
    for transaction in Transaction.objects.all():
        transaction.delete()

    for stock_purchase in StockPurchased.objects.all():
        stock_purchase.delete()

    for user_profile in UserProfile.objects.all():
        user_profile.balance = 200000
        user_profile.net_worth = 200000
        user_profile.save()


if __name__ == '__main__':
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SMS19.settings')
    django.setup()
    from main.models import Transaction, StockPurchased, UserProfile
    clean()
