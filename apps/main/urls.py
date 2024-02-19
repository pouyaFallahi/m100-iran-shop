# -*- coding: utf-8 -*-
from django.urls import path
from django.urls import path
from django.conf import settings
from .views import carousel_view
from django.conf.urls.static import static
from ..cart import views as views_cart
from ..User import views as views_user
from ..Product import views as views_product


urlpatterns = [
                path('', carousel_view, name='home_page'),
                path('user/login/', views_user.LogingView.as_view(), name='login_page', ),
                path('user/logout/', views_user.LogOutView.as_view(), name='logout_page'),
                path('user/signup', views_user.SignUpView.as_view(), name='signup_page'),
                path('product/', views_product.ShowAllItems.as_view(), name='item_cart', ),
                path('product/<int:pk>/', views_product.ShowItem.as_view(), name='item_detail'),
                path('product-list/api/', views_cart.show, name='show_cart_items'),
                path('category/<str:name_category>/', views_product.ShowItemByCategory.as_view(), name='item_by_category'),
                path('user/loginPhone/', views_user.LoginPhoneView.as_view(), name='loginPhone_page'),
                path('forgetPassword/', views_user.ChangePassWord.as_view(), name='forget_password'),
                path('user/signup/verify/email/', views_user.verify_email_view, name='verify_email_view'),
                path('user/email/accepted', views_user.verify_code, name='verify_code'),
                path('change-password/<hash>', views_user.change_password, name='change'),
                path('api/user/panel/<int:pk>/', views_user.show_customers_api_view, name='user_panel'),
                path('user/panel/<int:pk>/', views_user.ShowCustomersView.as_view(), name='user_panel'),
                path('product/search/', views_product.ProductSearch.as_view(), name='product_search'),
                path('product/api/<int:pk>/', views_cart.add_remove_item_cart_to_cookie, name='product_add_item_cart_aip'),
                # path('product/remove_all_orders/', views_product.remove_all_cart, name='remove_all'),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.
                                                                                           MEDIA_ROOT)
