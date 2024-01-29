import json

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
from .forms import CustomPasswordChangeForm, SignUpForm, PhoneNumberLoginForm, SubscribeForm

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
    success_url = reverse_lazy('verify_email')
    template_name = 'User/signup.html'

    # def post(self, request):
    #     email = request.POST.get('email')
    #     response = HttpResponse()
    #     response.set_cookie('email', json.dump(email))
    #     return response


def create_code():
    return ''.join(str(i) for i in range(10))


def verify_email_view(request):
    send_verification_email.delay('1380pouy@gmail.com', create_code())
    return
