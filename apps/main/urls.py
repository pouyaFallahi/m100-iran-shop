# -*- coding: utf-8 -*-
from django.urls import path
from .views import carousel_view
from django.conf import settings
from django.conf.urls.static import static
from ..User.views import LogingView, LogOutView, SignUpView, LoginPhoneView, change_password, verify_email_view, \
    verify_code
from ..Product.views import ShowAllItems, ShowItem, add_to_cart, remove_from_cart, show_cart_items, remove_all_cart, \
    ShowItemByCategory

urlpatterns = [
                  path('', carousel_view, name='home_page'),
                  path('user/login/', LogingView.as_view(), name='login_page', ),
                  path('user/logout/', LogOutView.as_view(), name='logout_page'),
                  path('user/signup', SignUpView.as_view(), name='signup_page'),
                  path('product/', ShowAllItems.as_view(), name='item_cart', ),
                  path('product/<int:pk>/', ShowItem.as_view(), name='item_detail'),
                  path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
                  path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
                  path('product/List_of_orders/', show_cart_items, name='show_cart_items'),
                  path('product/remove_all_orders/', remove_all_cart, name='remove_all'),
                  path('product/<str:name_category>/', ShowItemByCategory.as_view(), name='item_by_category'),
                  path('user/loginPhone/', LoginPhoneView.as_view(), name='loginPhone_page'),
                  path('forgetPassword/', change_password, name='forget_password'),
                  path('user/signup/verify/email/', verify_email_view, name='verify_email_view'),
                  path('user/email/accepted', verify_code, name='verify_code'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.
                                                                                           MEDIA_ROOT)
