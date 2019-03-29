"""SMS19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from main import views

killswitch_activate = True

if killswitch_activate:
    urlpatterns = [
        re_path('^.*$', views.killswitch, name="killswitch"),
    ]
else:
    urlpatterns = [

        path('accounts/logout/', views.user_logout, name='user_logout'),
        path('accounts/forgot_password/', views.user_forgot_password,
            name='user_forgot_password'),
        path('admin/', admin.site.urls),
        path('', views.game, name='game'),
        path('instructions/', views.instructions, name='instructions'),
        path('portfolio/', views.portfolio, name='portfolio'),
        path('efa/<code>/<pk>', views.api_efa, name='api_efa'),
        path('efa/<code>', views.api_efa, name='api_efa'),
        path('efa/', views.api_efa, name='api_efa'),
        path('buy_stock/<pk>/', views.buy_stock, name='buy_stock'),
        path('sell_stock/<pk>/', views.sell_stock, name='sell_stock'),
        path('accounts/register/', views.register, name='register'),
        path('accounts/login/', views.user_login, name='user_login'),
        path('test/', views.test, name="test"),
        path('get_stock_purchased/<str:code>', views.get_stock_purchased,
            name="get_stock_purchased"),
        path('get_news_post', views.get_news_post, name="get_news_post"),
        path('news', views.news, name="news"),
        path('leaderboard', views.leaderboard_data, name="leaderboard"),
        path('display_leaderboard', views.display_leaderboard,
            name='display_leaderboard'),
        path('get_stocks_data/<str:code>',
            views.get_stocks_data, name="get_stocks_data"),
        path('get_balance', views.get_balance, name="get_balance")
    ]
