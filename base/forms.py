from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True,
                             help_text='Required. Enter a valid email address.')
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full border rounded py-2 px-3 leading-tight focus:outline-none focus:shadow-outline'
    }))
    password = forms.CharField(widget = forms.PasswordInput(attrs={
        'class': 'w-full border rounded py-2 px-3 leading-tight focus:outline-none focus:shadow-outline'
    }))

