import json
from random import randint
from .models import User
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from .tasks import send_verification_email
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout, login, authenticate
from .forms import CustomPasswordChangeForm, SignUpForm, PhoneNumberLoginForm, SubscribeForm, VerifyEmailForm

count_of_logout = {}


class LoginPhoneView(View):
    form_class = PhoneNumberLoginForm
    template_name = 'User/login-phone.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_page')
            else:
                return render(request, self.template_name, {'form': form, 'error_message': _('Invalid login')})
        else:
            return render(request, self.template_name, {'form': form})


class LogingView(LoginView):
    template_name = 'User/login.html'
    success_url = reverse_lazy('home_page')


def change_password(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomPasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # نیاز است تا جلوی لاگ‌اوت از کاربر را بگیریم
                messages.success(request, _('Password changed!'))
                return redirect('login_page')
            else:
                messages.error(request, _('Please make the required corrections.'))
        else:
            form = CustomPasswordChangeForm(request.user)
        return render(request, 'User/forget_password.html', {'form': form})
    else:
        return HttpResponse(_('You do not have permission to access this section.'))


class LogOutView(View):
    def get(self, request):
        if self.request.user:
            user_login = request.user.email
            count_of_logout[user_login] = count_of_logout.get(user_login, 0) + 1
            logout(request)
            response = redirect('home_page')
            response.set_cookie('latest_user_login', user_login)
            response.set_cookie('count_of_logout', count_of_logout[user_login])
            response.delete_cookie('cart_data')
            return response


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('verify_email_view')
    template_name = 'User/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data['email']  # Assuming the email field in the form is named 'email'
        response.set_cookie('user_email', email)
        return response


def create_code():
    return str(randint(100000, 999999))


user_code = create_code()


def verify_email_view(request):
    user_email = request.COOKIES.get('user_email')
    code = user_code
    print(code)
    send_verification_email.delay(user_email, code)
    return render(request, 'User/verify_registration.html', {'form': VerifyEmailForm, 'code': code})


def verify_code(request):
    if request.method == 'POST':
        form = VerifyEmailForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == user_code:
                return redirect('login_page')
            else:
                return render(request, 'User/verify_registration.html',
                              {'form': VerifyEmailForm, 'code': code, 'message': 'code is not correct'})
        else:
            return render(request, 'User/verify_registration.html', {'form': VerifyEmailForm, 'code': 123456})
    else:
        return render(request, 'User/verify_registration.html', {'form': VerifyEmailForm, 'code': 123456})
