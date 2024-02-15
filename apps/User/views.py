from .models import User
from random import randint
from django.core import signing
from django.utils import timezone
from django.contrib import messages
from ..main.models import OneTimeURL
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render
from rest_framework.response import Response
from ..main.views import generate_one_time_url
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from .serializers import UserSerializer
from rest_framework.request import Request
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, View, FormView, DetailView, UpdateView
from .tasks import send_verification_email, send_email_for_change_password
from django.contrib.auth import update_session_auth_hash, logout, login, authenticate, update_session_auth_hash
from .forms import CustomPasswordChangeForm, SignUpForm, PhoneNumberLoginForm, SubscribeForm, VerifyEmailForm, \
    EditUserForm
from rest_framework.decorators import api_view

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
    success_url = reverse_lazy('enter_code')
    template_name = 'User/signup.html'

    def form_valid(self, form):
        sign = signing.TimestampSigner()
        response = super().form_valid(form)
        email = form.cleaned_data['email']  # Assuming the email field in the form is named 'email'
        email = sign.sign_object(email)
        response.set_cookie('user_email', email)
        return response


def create_code():
    return str(randint(100000, 999999))


user_code = create_code()


def verify_email_view(request):
    sig = signing.TimestampSigner()
    user_email = request.COOKIES.get('user_email')
    user_email = sig.unsign_object(user_email)
    code = user_code
    print(code, user_email)
    send_verification_email.delay(user_email, code)
    return render(request, 'User/verify_registration.html', {'form': VerifyEmailForm, 'code': code})


def change_password(request):
    sign = signing.TimestampSigner()
    user_email = request.COOKIES.get('user_email')
    user_email = sign.unsign_object(user_email)
    if user_email in User.email:
        return HttpResponse('True')
    else:
        return HttpResponse('True')


class ChangePassWord(FormView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('change')
    template_name = 'User/forget_password.html'

    def form_valid(self, form):
        sign = signing.TimestampSigner()
        response = super().form_valid(form)
        email = form.cleaned_data['email_fild']
        send_email_for_change_password.delay(email)
        email = sign.sign_object(email)
        response.set_cookie('user_email', email)


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


@api_view(['GET', 'PUT'])
def show_customers_api_view(request: Request, pk):
    if request.method == 'GET':
        user = User.objects.get(pk=pk)
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)

    if request.method == 'PUT':
        pass


class ShowCustomersView(DetailView):
    model = User
    template_name = 'User/customers.html'


def get(self, requset, *args, **kwargs):
    user = requset.user
    if user.is_authenticated:
        if kwargs['pk'] == user.id:
            return super().get(requset, *args, **kwargs)
        else:
            return redirect('home_page')

    else:
        return redirect('home_page')


class EditProfileView(UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'User/edit-file.html'
    success_url = reverse_lazy('home_page')
