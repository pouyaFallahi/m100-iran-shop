from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import logout, login
from .tasks import send_verification_email
from django.shortcuts import redirect, render
from .forms import UserCreationForm, SignUpForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, View, edit




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





