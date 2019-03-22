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
from django.urls import path, include
from main import views
from django.conf.urls import url


urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.game, name='game'),
    path('profile/', views.profile, name='profile'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('delete_stock/<pk>/', views.delete_stock, name='delete_stock'),
    path('add_newspost/', views.add_newspost, name='add_newspost'),
    path('delete_newspost/<pk>/', views.delete_newspost, name='delete_newspost'),
    path('buy_stock/<pk>/', views.buy_stock, name='buy_stock'),
    path('sell_stock/<pk>/', views.sell_stock, name='sell_stock'),
    path('accounts/', include('allauth.urls')),
    path('test/', views.test, name="test")
]
