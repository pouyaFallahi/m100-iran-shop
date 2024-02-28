from random import randint
from django.core import signing
from rest_framework import status
from django.http import HttpResponse
from django.urls import reverse_lazy
from .serializers import UserSerializer
from .models import User, PasswordReset
from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import logout, login, authenticate
from .tasks import send_verification_email, send_email_for_change_password
from django.views.generic import CreateView, View, FormView, DetailView, UpdateView
from .forms import CustomPasswordChangeForm, SignUpForm, PhoneNumberLoginForm, VerifyEmailForm, EditUserForm, \
    ChangePasswordForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = "wellcome"
        return context


class LogOutView(View):
    def get(self, request):
        if self.request.user:
            user_login = request.user.email
            count_of_logout[user_login] = count_of_logout.get(user_login, 0) + 1
            logout(request)
            response = redirect('home_page')
            # response.set_cookie('latest_user_login', user_login)
            response.set_cookie('count_of_logout', count_of_logout[user_login])
            response.delete_cookie('cart_data')
            return response


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('verify_email_view')
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
    send_verification_email.delay(user_email, code)
    return render(request, 'User/verify_registration.html', {'form': VerifyEmailForm, 'code': code})


def change_password(request):
    try:
        sign = signing.TimestampSigner()
        user_email = request.COOKIES.get('user_email')
        user_email = sign.unsign_object(user_email)
        if User.objects.get(email=user_email):
            return HttpResponse('True')
    except User.DoesNotExist:
        return HttpResponse('False')


class ChangePassWord(FormView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('email_send')
    template_name = 'User/forget_password.html'

    def post(self, request, *args, **kwargs):
        user = User()
        if user.is_anonymous:
            return render(request, 'User/no_access.html')
        else:
            sign = signing.TimestampSigner()  # This method is used to hash email
            form = self.get_form()
            if form.is_valid():
                email = form.cleaned_data['email_fild']
                print(email)
                user = User.objects.filter(email=email).first()
                if user:
                    token = get_random_string(length=32)
                    password_reset = PasswordReset.objects.create(user=user, token=token)
                    password_reset.save()
                    reset_link = request.build_absolute_uri('/') + f'password_reset/{token}/'
                    send_email_for_change_password.delay(email, reset_link)
                    return redirect('home_page')
            else:
                return self.form_invalid(form)


def reset_password(request, token):
    if request.method == 'POST':
        password_reset = PasswordReset.objects.filter(token=token, is_active=True).first()
        if password_reset:
            user = User.objects.get(email=password_reset.user.email)
            new_password = request.POST.get('password')  # دریافت رمز عبور جدید از فرم

            # تغییر رمز عبور کاربر
            user.set_password(new_password)
            user.save()

            # غیرفعال کردن کد فعال‌سازی
            password_reset.is_active = False
            password_reset.save()

    return render(request, 'User/forget_password_form.html', context={'form': ChangePasswordForm})


def email_send(request):
    if request.COOKIES.get('user_email'):
        sign = signing.TimestampSigner()  # This method is used to hash email
        email = request.COOKIES.get('user_email')
        email = sign.unsign_object(email)
        user_email = User.objects.filter(email=email)
        for emails in user_email:
            if email == emails.email:
                return render(request, 'User/Email_send.html', {'messages': _('check your mail')})
        else:
            return render(request, 'User/Email_send.html', {'messages': _('No such email was found')})
    else:
        return render(request, 'User/Email_send.html', {'messages': _('no access')})


def verify_code(request):
    if request.method == 'POST':
        form = VerifyEmailForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == user_code:
                sig = signing.TimestampSigner()
                user_email = request.COOKIES.get('user_email')
                user_email = sig.unsign_object(user_email)
                user = get_object_or_404(User, email=user_email)
                user.is_active = True
                user.save()
                return render(request, 'home-page.html', {'messages': _('You have successfully registered')})
            else:
                return render(request, 'User/verify_registration.html',
                              {'form': VerifyEmailForm, 'code': code, 'message': 'code is not correct'})
        else:
            return render(request, 'User/verify_registration.html', {'form': VerifyEmailForm, 'code': create_code()})
    else:
        return render(request, 'User/verify_registration.html', {'form': VerifyEmailForm, 'code': create_code()})


@api_view(['GET', 'PUT'])
def show_customers_api_view(request: Request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
