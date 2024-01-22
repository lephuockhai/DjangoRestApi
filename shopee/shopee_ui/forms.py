from django import forms
from .models import CustomUser, CartInfomation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):

    class Meta:
        model = CustomUser
        fields= ['username', 'password']

class AddToCartForm(forms.ModelForm):

    class Meta:
        model = CartInfomation
        fields = ['quantity']

