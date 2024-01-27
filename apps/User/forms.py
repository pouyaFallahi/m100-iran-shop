from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number']


class YourForm(forms.Form):
    your_field = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'aria-label': 'Sizing example input',
                                      'aria-describedby': 'inputGroup-sizing-default'})
    )


class SignUpFormEmail(UserCreationForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number']


class SubscribeForm(forms.Form):
    email = forms.EmailField()
    message = forms.CharField(label='check your mail')


class PhoneNumberLoginForm(forms.Form):
    phone_number = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
