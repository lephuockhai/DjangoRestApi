from django.urls import re_path, include, path
from django.contrib.auth import views as auth_views

from .views import (
    LoginAPI,
    get_profile,
    RegisterAPIView,
    ProductList,
    CategoryList,
    get_homepage_category,
    add_to_cart,
    product_detail_page,
    get_cart,
    add_purchase,
    add_schedule,
    cart_update,
    delete_cart,
    add_purchase_detail,
    ship_info,
    payment,
)   

urlpatterns = [
    path('v1/login-api/', LoginAPI, name='login-api'),
    path('v1/account/get_profile/', get_profile, name= 'get_profile'),
    path('register/', RegisterAPIView.as_view(), name= 'api-register'),
    path('v1/product_list/', ProductList, name='product_list'),
    path('v1/pages/get_homepage_category/', get_homepage_category, name='get_homepage_category'),
    path('v1/pages/categories/<int:catid>/', CategoryList, name='category_call'),
    path('v1/add_to_cart/', add_to_cart, name= 'add_to_cart'),
    path('v1/product_detail_page/', product_detail_page, name='product_detail_page'),
    path('v1/cart/', get_cart, name= 'cart'),
    path('v1/cart/add_purchase/', add_purchase, name= 'add_purchase'),
    path('v1/cart/add_schedule/', add_schedule, name= 'add_schedule'),
    path('v1/cart/cart_update/', cart_update, name= 'cart_update'),
    path('v1/cart/delete_cart/', delete_cart, name= 'delete_cart'),
    path('v1/cart/add_purchase_detail/', add_purchase_detail, name= 'add_purchase_detail'),
    path('v1/cart/ship_info/', ship_info, name= 'ship_info'),
    path('v1/cart/payment/', payment, name= 'payment'),
    
    
    # path('login/', lo_gin, name='login'),

    # path('register/', Register, name='register'),
    # path('login/', lo_gin, name='login')

    # main URLS
    # path('', home, name='home page'),

    # # user URLs
    # path('signup/', signup, name='signup account'),
    # path('login/', login, name='login'),
    # path('user/update_info/<int:user_id>/', update_info, name= 'update info'),
    # path('user/get_info/<int:user_id>/', get_info, name='get info'),

    # # categories, products, shipping cart URLs
    # path('categories/<int:categori_id>/',product_in_category, name='product in category'),
    # path('shop/<int:shop_id>/add-product/',add_product, name='add product'),
    # path('shop/<int:shop_id>/modify_product/<product_id>/', modify_product, name= 'modify product'),
    # path('products/<int:product_id>/',product_info, name='get info product with product_id'),
    # path('shop/<int:shop_id>/modify-product/<int:product_id>/',modify_product, name='modify product'),
    # path('shop/<int:shop_id>/delete-product/<int:product_id>/',delete_product, name='delete product'),
    
    # # shipping cart
    # path('cart/<int:user_id>/add-to-cart/', add_to_cart, name='add product to cart'),
    # path('cart/<int:user_id>/delete-from-cart/', delete_from_cart, name='delete product from cart'),
    # path('cart/<int:user_id>/modify-cart/', modify_cart, name='modify product from cart'),

    # # order of user
    # path('user/<int:user_id>/purchase/',orders, name='show all order'),
    # # path('user/<int:user_id>/get-purchase/<int:order_id>/',get_order, name='get order'),
    # path('user/<int:user_id>/add-order/',add_order, name='add order'),
    # path('user/<int:user_id>/cancel-order/',cancel_order, name='cancel order'),

    # path('api/register', UserRegisterView.as_view(), name='register'),
    # path('api/login', jwt_views.TokenObtainPairView.as_view(), name='login'),

    # administration
    
]