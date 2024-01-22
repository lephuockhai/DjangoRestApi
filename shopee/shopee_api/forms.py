from django import forms
from .models import CustomUser, OrderDetail
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields= ['username', 'password']

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Enter a valid email address.')
    class Meta:
        model= CustomUser
        fields= ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'date_of_birth', 'gender']


