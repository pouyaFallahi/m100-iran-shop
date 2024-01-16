from django.contrib import admin
from django.urls import path
from .views import homepage
from ..User.views import LogingView, LogOutView,SignUpView

urlpatterns = [
    path('', homepage, name='home_page'),
    path('user/login/', LogingView.as_view(), name='login_page'),
    path('user/logout/', LogOutView.as_view(), name='logout_page'),
    path('user/signup', SignUpView.as_view(), name='signup_page')
]
