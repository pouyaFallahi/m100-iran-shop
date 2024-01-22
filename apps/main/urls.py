# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path
from .views import homepage
from ..User.views import LogingView, LogOutView, SignUpView
from ..Product.views import ShowAllItems, ShowItem, add_to_cart, remove_from_cart, show_cart_items, remove_all_cart

urlpatterns = [
    path('', homepage, name='home_page'),
    path('user/login/', LogingView.as_view(), name='login_page'),
    path('user/logout/', LogOutView.as_view(), name='logout_page'),
    path('user/signup', SignUpView.as_view(), name='signup_page'),
    path('product/', ShowAllItems.as_view(), name='item_cart'),
    path('product/<int:pk>/', ShowItem.as_view(), name='item_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('product/List_of_orders/', show_cart_items, name='show_cart_items'),
    path('product/remove_all_orders/', remove_all_cart, name='remove_all'),
]
