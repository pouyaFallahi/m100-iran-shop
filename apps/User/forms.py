from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class YourForm(forms.Form):
    your_field = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'aria-label': 'Sizing example input',
                                      'aria-describedby': 'inputGroup-sizing-default'})
    )


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number']
