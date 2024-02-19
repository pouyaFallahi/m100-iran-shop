from django import forms
from .models import Product



class FormSearchItem(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
