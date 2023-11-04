from django.urls import re_path, include
from .views import create_account, login, update_info, get_info

urlpatterns = [
    re_path('create_account', create_account, name='create account'),
    re_path('login', login, name='login'),
    re_path('update_info', update_info, name= 'update info'),
    re_path('get_info', get_info, name='get info'),
]