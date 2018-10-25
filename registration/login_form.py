from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput)

    # class Meta:
    #     model = User
        # fields = ("username", "password1", "password2")