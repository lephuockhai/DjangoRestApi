from django.urls import path, include
from .views import (RegisterView, 
                    LoginView, 
                    LogoutView, 
                    home, 
                    Categories_Page,
                    Product_page,
                    payment,)

urlpatterns = [
    path('register/', RegisterView, name='register'),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('home/', home, name= 'home'),
    path('cat/<int:catid>/', Categories_Page, name='Categories_Page'),
    path('Product_Page/<int:product_id>/', Product_page, name='Product_page'),
    path('cart/payment/', payment, name= 'payment'),
]