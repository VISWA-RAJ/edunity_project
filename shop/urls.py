# shop/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Main shop page: /shop/
    path('', views.shop_home_view, name='shop'),
    
    # Action for buying an item: /shop/buy/5/
    path('buy/<int:item_id>/', views.buy_item_view, name='buy_item'),
]
