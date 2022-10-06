from django import forms
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, initial=False,
                                widget=forms.PasswordInput)