from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'phone_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control form-control-lg', 'type': 'text', 'placeholder': _('User Name'),
                       'aria-label': 'User Name'}),
            'full_name': forms.TextInput(
                attrs={'class': 'form-control form-control-lg', 'type': 'text', 'placeholder': _('Full Name'),
                       'aria-label': 'Full Name'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control form-control-lg', 'type': 'email', 'placeholder': _('Email'),
                       'aria-label': 'Email'}),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control form-control-lg', 'type': 'text', 'placeholder': _('Phone Number'),
                       'aria-label': 'Phone Number'}),
            'password1': forms.PasswordInput(
                attrs={'class': 'form-control form-control-lg', 'type': 'password', 'placeholder': _('Password'),
                       'aria-label': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'type': 'password',
                                                    'placeholder': _('Confirm Password'),
                                                    'aria-label': 'Confirm Password'}),
        }


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
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'type': 'text', 'placeholder': _('Phone Number'),
               'aria-label': 'Phone Number'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg', 'type': 'password', 'placeholder': _('Password'),
               'aria-label': 'Password'}))


class CustomPasswordChangeForm(forms.Form):
    email_fild = forms.EmailField(label='email', widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-lg', 'type': 'email', 'placeholder': _('Email'),
               'aria-label': 'Email'}))


class VerifyEmailForm(forms.Form):
    code = forms.CharField(label='code', widget=forms.EmailInput(
                attrs={'class': 'form-control form-control-lg', 'type': 'text', 'placeholder': _('Code'),
                       'aria-label': 'code'}),

    )


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'address']
        widgets = {
            'full_name': forms.TextInput(
                attrs={'class': 'form-control form-control-lg', 'type': 'text', 'placeholder': _('Full Name'),
                       'aria-label': 'Full Name'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control form-control-lg', 'type': 'email', 'placeholder': _('Email'),
                       'aria-label': 'Email'}),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control form-control-lg', 'type': 'text', 'placeholder': _('Phone Number'),
                       'aria-label': 'Phone Number'}),
            'address': forms.TextInput(
                attrs={'class': 'form-control form-control-lg', 'type': 'text', 'placeholder': _('Address'),
                       'aria-label': 'Address'}),
        }



