from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, AddToCartForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseNotFound
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView, api_view

#MyModel
from MyModel.MyFunction import CallRequest
# register account
@permission_classes([AllowAny])
def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            api_url = 'http://localhost:8001/shopee/api/register/'  # Thay đổi URL tùy theo cấu hình của bạn
            data = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password1'],
                'password2': form.cleaned_data['password2'],
            }
            response = requests.post(api_url, data=data)
            print(response.text)
            if response.status_code == 201:
                return redirect('login')
            else:
                error_message = f"Failed to register. Server error: {response.text}"
                form.add_error(None, error_message)
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

# login
@csrf_exempt
def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request= request, username= username, password= password)
            if user is not None:
                login(request=request, user=user)
                user_url = 'http://127.0.0.1:8001/shopee/api/v1/login-api/'
                response = requests.post(url=user_url, data={'username': username, 'password': password})
                if response.status_code == 200:
                    response_data = response.json().get('response_data')
                    access = response_data['access']
                    request.session['token'] = access
                    print('token login view: ',access)
                    headers = {'Authorization': f'Bearer {access}'}
                    profile_url = 'http://127.0.0.1:8001/shopee/api/v1/account/get_profile/'
                    response = requests.get(url= profile_url, headers= headers)
                    if response.status_code == 200:
                        user_info = response.json().get('user_data')
                    else:
                        print('Error get:', response.status_code)
                    return redirect('home')
                else:
                    print('Error post:', response.status_code)
            else:
                return Response('Page not found', status= status.HTTP_404_NOT_FOUND)
        else:
            print('form errors: ',form.errors)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def LogoutView(request):
    logout(request)
    return redirect('login')

# get data for home page
@login_required
@permission_classes([IsAuthenticated])
def home(request):
    if request.method == 'GET':
        product = request.GET.get('product')
        print("product name: ", product)
        cat_url = 'http://127.0.0.1:8001/shopee/api/v1/pages/get_homepage_category/'
        response1 = requests.get(url= cat_url)
        if response1.status_code == 200:
            cat_list = response1.json().get('cat_list')
        else:
            print("error category: ",response1.status_code)

        api_url = 'http://127.0.0.1:8001/shopee/api/v1/product_list/'
        response = requests.get(url= api_url, params={'product': product, 'is_homepage': True})
        if response.status_code == 200:
            products = response.json().get('products')
            message = response.json().get('message')
            print(message)
        else:
            print("error product: ",response.status_code)
    return render(request, 'home.html',{'categories': cat_list, 'products': products, 'message': message})

# categories and product of parent category
def Categories_Page(request, catid):
    if request.method == 'GET':
        product = request.GET.get('product')
        api_url = 'http://127.0.0.1:8001/shopee/api/v1/product_list/'
        response = requests.get(url= api_url, params={'product': product, 'catid': catid, 'is_homepage': False})
        if response.status_code == 200:
            products = response.json().get('products')
        else:
            print(response.status_code)
        cat_url = 'http://127.0.0.1:8001/shopee/api/v1/pages/categories/' + str(catid) + '/'
        response1 = requests.get(url= cat_url)
        if response1.status_code == 200:
            cat_list = response1.json().get('categories')
        else:
            print(response1.status_code)
    return render(request, 'category.html',{'cat_list': cat_list, 'products': products})

# infomation of product selected
def Product_page(request, product_id):
    url_prod = 'http://127.0.0.1:8001/shopee/api/v1/product_detail_page/'
    response = requests.get(url= url_prod, params={'product_id': product_id})
    if response.status_code == 200:
        product = response.json().get('product')
    else:
        print('error product', response.status_code)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():

            user_id = request.user.id
            first_product = product[0] if product else {}

            quantity = form.cleaned_data['quantity']
            price = first_product.get('price', 0)
            # Lấy token từ cookie
            token = request.session.get('token')
            headers = {'Authorization': f'Bearer {token}'}
            print(token)
            data = {'user_id': user_id, 'product_id': product_id, 'quantity': quantity, 'price': price}
            url_addtocart = 'http://127.0.0.1:8001/shopee/api/v1/add_to_cart/'
            respone1 = requests.post(url= url_addtocart, data= data, headers= headers)
            if respone1.status_code == 200:
                cart_count = respone1.json().get('cart_count')
                print(cart_count)
                return redirect('Product_page', product=product, cart_count=cart_count)

            else:
                print('error cart', respone1.status_code)
        else:
            print('error form:', form.errors)
    else:
        form = AddToCartForm()
    return render(request, 'product.html',{'product': product, 'form': form})

# def api_request(base_url, endpoint, data, headers):
#     url = f'{base_url}{endpoint}/'
#     response = requests.post(url=url, params=data, headers= headers)
#     if response.status_code == 200:
#         print('Successful')
#     else:
#         print(f'Error {endpoint} - Status Code: {response.status_code}')

# def api_repsonse(url, data, headers):
#     response = requests.post(url=url, params=data, headers= headers)
#     if response.status_code == 200:
#         data_response = response.json()
#         print(data_response)
#         return data_response
#     else:
#         print(f'Error {url} - Status Code: {response.status_code}')
#         return None

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment(request):
    if request.method == 'POST':
        user_id = request.user.id
        data = request.data.get('data')
        products = data.get('products')
        shipping_info = data.get('shipping_info')
        payment_info = data.get('payment_info')
        token = request.session.get('token')
        headers = {'Authorization': f'Bearer {token}'}
        
        data_order = {
            "user_id": user_id,
            "total_amount": data.get('total_amount'),
            "voucher_discount": data.get('voucher_discount'),
            "voucher_id": data.get('voucher_id'),
            "final_amount": data.get('final_amount')
        }


        API_BASE_URL_CART = 'http://127.0.0.1:8001/shopee/api/v1/cart/'

        # 1. create order to get order_id
        response_order = CallRequest(base_url= API_BASE_URL_CART, endpoint= 'add_purchase', data= data_order, headers= headers)
        order_id = response_order.get('order_id')

        # 2. add detail of product to order detail
        for product in products:
            data_order_detail = {
            'order_id': order_id,
            'product_id': product['product_id'],
            'price': product['price'],
            'quantity': product['quantity'],
            'total': product['total'],
            }

            response_order_detail = CallRequest(base_url= API_BASE_URL_CART, endpoint= 'add_purchase_detail', data= data_order_detail, headers= headers)
            

        # 3. add ship info
        data_ship_info = {
        'order_id': order_id,
        'recipient_name': shipping_info['name'],
        'recipient_phone': shipping_info['phone'],
        'recipient_adress': shipping_info['address'],
        }
        response_ship_info = CallRequest(base_url= API_BASE_URL_CART, endpoint= 'ship_info', data= data_ship_info, headers= headers)

        # 4. add payment info
        data_payment = {
        'order_id': order_id,
        'method': payment_info.get('method'),
        'status_pay': payment_info.get('status_pay'),
        'final_amount': data.get('final_amount')
        }
        print(data_payment)
        response_payment = CallRequest(base_url= API_BASE_URL_CART, endpoint= 'payment', data= data_payment, headers= headers)
            
        # 5. add shipping schedule
        data_schedule = {
            'order_id': order_id,
            'schedule': 'Thanh toán thành công',
        }
        response_schedule = CallRequest(base_url= API_BASE_URL_CART, endpoint= 'add_schedule', data= data_schedule, headers= headers)
        message = response_schedule.get('message')
        return JsonResponse({'message': message})

    return JsonResponse({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)
        