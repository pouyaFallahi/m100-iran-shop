from django.urls import reverse_lazy
from django.http import HttpResponse
from .tasks import send_verification_email
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, View, edit
from django.contrib.auth.decorators import login_required
from .forms import UserCreationForm, SignUpForm, PhoneNumberLoginForm
from .models import User


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
                return render(request, self.template_name, {'form': form, 'error_message': 'Invalid login'})
        else:
            return render(request, self.template_name, {'form': form})


class LogingView(LoginView):
    template_name = 'User/login.html'
    success_url = reverse_lazy('')


count_of_logout = {}


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
    success_url = reverse_lazy('login_page')
    template_name = 'User/signup.html'


def verify_registration(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            request.user.profile.verified = True
            request.user.save()

            return render(request, 'User/verification_success.html')
    else:
        form = VerificationForm()

    return render(request, 'User/verify_registration.html', {'form': form})


def authentication_email(request):
    verification_code = '123456'

    send_verification_email.delay(request.user.email, verification_code)

    return HttpResponse('Verification email sent!')


class ForgetPasswordView(edit.UpdateView):
    model = User
    form_class = UserCreationForm
    template_name = 'User/forget_password.html'
    success_url = reverse_lazy('login_page')

    def get(self, request, *args, **kwargs):
        return render(self.request, 'User/forget_password.html')
