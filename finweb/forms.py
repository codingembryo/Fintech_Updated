from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



class SignUpForm(UserCreationForm):

    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))

    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))

    first_name = forms.CharField(label="", max_length="100", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    
    last_name = forms.CharField(label="", max_length="100", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))


class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')