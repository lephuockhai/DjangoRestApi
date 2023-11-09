from django.urls import re_path, include, path
from .views import signup, login, get_info, update_info

urlpatterns = [
    path('signup', signup, name='signup account'),
    path('login', login, name='login'),
    path('update_info', update_info, name= 'update info'),
    path('get_info', get_info, name='get info'),
]