# call modul rest_framework
from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
# call modul django
from django.db import connection
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from .serializer import UserLoginSerializer, RegisterSerializer
from .models import ProductInfomation

import json
from decimal import Decimal

#mymodel
from MyModel.MyFunction import ConnectByExcu, ConnectByProd, Caching

@permission_classes([AllowAny])
class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def LoginAPI(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request= request, username= username, password= password)
        if user is not None:
            login(request=request, user=user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            response_data = {
                'access': access_token,
                'refresh': refresh_token,
            }
            return JsonResponse({'response_data': response_data}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'errors': 'Invalid credentials'}, status= status.HTTP_401_UNAUTHORIZED)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    if request.method == 'GET':
        user = request.user
        print(request)
        if user is not None and user.is_authenticated:
            cache_key = f"user_profile:{user.id}"
            user_info = {
                    'user_id': user.id,
                    'username': user.username,
                    'phone': user.phone,
                    'date_of_birth': user.date_of_birth,
                    'gender': user.gender,
                    'email': user.email
                }
            result = Caching(key= cache_key, data= user_info, timeout= 60*60)
            return JsonResponse({'user_data': result}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    
    return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)

# get product
def get_product(cat_id = 0, limit=10, offset=0, is_homepage=False):
    procedure_name = 'product_homepage' if is_homepage else 'product_category'
    with connection.cursor() as cursor:
        cursor.callproc(procedure_name, (cat_id, limit, offset,))
        results = cursor.fetchall()
        products = [{
            "id": result[0],
            "name": result[1],
            "description": result[2],
            "cat_id": result[3],
            "price": result[4],
            "stock": result[5],
            "shop_id": result[6],
            "sold": result[7],
            "brand": result[8],
            "price_min": result[9],
            "historical_sold": result[10],
            "liked_count": result[11],
            "image": result[12],
            "images": json.loads(result[13])
        } for result in results]
    return products

def product_detail(prod_id = 0):
    query = 'SELECT id, name, description, cat_id, price, stock, shop_id, sold, brand, price_min, historical_sold, liked_count, image, images FROM products WHERE id = %s;'
    with connection.cursor() as cursor:
        cursor.execute(query, (prod_id,))
        results = cursor.fetchall()
        products = [{
            "id": result[0],
            "name": result[1],
            "description": result[2],
            "cat_id": result[3],
            "price": result[4],
            "stock": result[5],
            "shop_id": result[6],
            "sold": result[7],
            "brand": result[8],
            "price_min": result[9],
            "historical_sold": result[10],
            "liked_count": result[11],
            "image": result[12],
            "images": json.loads(result[13])
        } for result in results]
    return products

def get_cat(parent_id = 0):
    categories = []
    cache_key = "cat" + str(parent_id)
    if cache.get(cache_key):
        categories = cache.get(cache_key)
    else:
        with connection.cursor() as cursor:
            cursor.callproc('cat_list', (parent_id,))
            results = cursor.fetchall()

        for result in results:
            if result[2] == parent_id:
                categories.append({
                    "catid": result[0],
                    "name": result[1],
                    "parent_id": result[2],
                    "display_name": result[3],
                    "level": result[4],
                    "image": result[5]
                })
        cache.set(key= cache_key, value= categories)

    return categories

def search_product(fillter_product = None):
    products = []

    if fillter_product:
        with connection.cursor() as cursor:
            cursor.callproc('search_product', (fillter_product, 10, 0))
            results = cursor.fetchall()
            products = [{
                "id": result[0],
                "name": result[1],
                "description": result[2],
                "cat_id": result[3],
                "price": result[4],
                "stock": result[5],
                "shop_id": result[6],
                "sold": result[7],
                "brand": result[8],
                "price_min": result[9],
                "historical_sold": result[10],
                "liked_count": result[11],
                "image": result[12],
                "images": json.loads(result[13])
            } for result in results]
    else:
        products = get_product()

    return products

def CacheProduct(key = None ,exp = 150, is_homepage = False, catid = 0):
    print(is_homepage)
    if key:
        if cache.get(key= key):
            result = cache.get(key= key)
            ttl = cache.ttl(key)
            print("ttl: " ,ttl)
            message = "Data From Cache"
        else:
            result = search_product(fillter_product= key)
            cache.set(key= key, value= result,timeout= exp)
            message = "Data From DB saved to Cache"
            ttl = cache.ttl(key)
    else:
        result = get_product(cat_id= catid, is_homepage= is_homepage)
        message = "Random from DB"
        ttl = 0
    return result, message, ttl

# home page
def ProductList(request):
    if request.method == 'GET':
        fillter_product = request.GET.get('product')
        is_homepage = request.GET.get('is_homepage')
        catid = request.GET.get('catid') if request.GET.get('catid') else 0

        products, message, ttl = CacheProduct(key= fillter_product, is_homepage= is_homepage, catid= catid)
        return JsonResponse({'message': message, 'ttl': ttl, 'products': products}, status=status.HTTP_200_OK)

def CategoryList(request, catid):
    if request.method == 'GET':
        categories = get_cat(parent_id= catid)
        return JsonResponse({'categories': categories}, status=status.HTTP_200_OK)
    
def get_homepage_category(request):
    if request.method == 'GET':
        cat_list = get_cat()
    return JsonResponse({'cat_list': cat_list}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    if request.method == 'POST':
        
        cart_id = ConnectByExcu(query= 'SELECT MAX(id) FROM shipping_carts;')

        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        price = request.data.get('price')

        data = (cart_id, user_id, product_id, quantity, price,)
        result = ConnectByProd(prod_name= 'prod_add_to_cart', data= data)
        return JsonResponse({'cart_count': result[0]})
    else:
        print('error not post')
        return JsonResponse({'cart_count': 0})
           
##
def product_detail_page(request):
    if request.method == 'GET':
        product_id = request.GET.get('product_id')
        result = product_detail(prod_id= product_id)
        return JsonResponse({'product': result}, status= status.HTTP_200_OK)
    
@csrf_exempt
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def get_cart(request):
    if request.method == 'GET':
        user_id = request.user.id
        results = ConnectByProd(prod_name= 'get_cart', data= (user_id,))
        products = [{
        "product_id": result[0],
        "name": result[1],
        "quantity": result[2],
        "price": result[3],
        "total": result[4]
        } for result in results]
        return JsonResponse({'cart': products}, status= status.HTTP_200_OK)
    return JsonResponse({'error': 'not get'}, status= status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['POST']) 
@permission_classes([IsAuthenticated])
def cart_update(request):
    if request.method == 'POST':
        product_id = request.data.get('product_id')
        user_id = request.user.id

        query = 'SELECT quantity FROM shipping_carts WHERE user_id = %s AND product_id = %s;'
        data = (user_id, product_id,)
        quantity = ConnectByExcu(query= query, data= data)
        action = request.data.get('action')

        if action == 'inscrease':
            quantity += 1
        elif action == 'decrease':
            if quantity >1:
                quantity -= 1
                new_list = ConnectByProd(prod_name= 'cart_update', data= (user_id, product_id, quantity,))
            else:
                new_list = ConnectByProd(prod_name= 'delete_cart', data= (user_id, product_id,))
                return JsonResponse({'new_list': new_list}, status= status.HTTP_200_OK)
            
        return JsonResponse({'new_list': new_list}, status= status.HTTP_200_OK)
    return JsonResponse({'error': 'not post'}, status= status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_cart(request):
    if request.method == 'POST':
        product_id = request.data.get('product_id')
        user_id = request.user.id

        new_list = ConnectByProd(prod_name= 'delete_cart', data= (user_id, product_id,))

        return JsonResponse({'new_list': new_list}, status= status.HTTP_200_OK)
    return JsonResponse({'error': 'not post'}, status= status.HTTP_404_NOT_FOUND)



@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_purchase(request):
    if request.method == 'POST':
        query = 'SELECT (COALESCE(MAX(id), 0) + 1) FROM orders;'
        order_id = ConnectByExcu(query= query)
        order_id = order_id[0][0]
        print(order_id)
            
        now = datetime.now()
        create_at = now.strftime("%Y-%m-%d %H:%M:%S")
        user_id = request.user.id
        total_amount = Decimal(request.data.get('total_amount'))
        voucher_discount = Decimal(request.data.get('voucher_discount'))
        voucher_id = request.data.get('voucher_id')
        final_amount = Decimal(request.data.get('final_amount'))
        data = (order_id, user_id, create_at, total_amount, voucher_discount, voucher_id, final_amount,)
        result = ConnectByProd(prod_name= 'create_order', data= data)

        return JsonResponse({'order_id': order_id, 'message': result}, status= status.HTTP_200_OK)
    return JsonResponse({'message': 'Invalid request method'}, status=400)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_purchase_detail(request):
    if request.method == 'POST':
        query = 'SELECT (COALESCE(MAX(id), 0) + 1) FROM order_detail;'
        id = ConnectByExcu(query= query)
        id = id[0][0]

        order_id = request.data.get('order_id')
        product_id = request.data.get('product_id')
        price = Decimal(request.data.get('price'))
        quantity = request.data.get('quantity')
        total = Decimal(request.data.get('total'))
        
        data = (id, order_id, product_id, price, quantity, total,)
        result = ConnectByProd(prod_name= 'add_detail_order', data= data)
        
        return JsonResponse({'message': result}, status= status.HTTP_200_OK)
    return JsonResponse({'message': 'Invalid request method'}, status=400) 

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ship_info(request):
    if request.method == 'POST':
        query = 'SELECT (COALESCE(MAX(id), 0) + 1) FROM shipping_info;'
        id = ConnectByExcu(query= query)
        id = id[0][0]

        order_id = request.data.get('order_id')
        recipient_name = request.data.get('recipient_name')
        recipient_adress = request.data.get('recipient_adress')
        recipient_phone = request.data.get('recipient_phone')
        data = (id, order_id, recipient_name, recipient_adress, recipient_phone,)
        result = ConnectByProd(prod_name= 'add_shipping_info', data= data)
        
        return JsonResponse({'message': result}, status= status.HTTP_200_OK)
    return JsonResponse({'message': 'Invalid request method'}, status=400)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment(request):
    if request.method == 'POST':
        query = 'SELECT (COALESCE(MAX(id), 0) + 1) FROM order_payment;'
        id = ConnectByExcu(query= query)
        id = id[0][0]

        order_id = request.data.get('order_id')
        now = datetime.now()
        create_at = now.strftime("%Y-%m-%d %H:%M:%S")
        method = request.data.get('method')
        status_pay =request.data.get('status_pay')
        final_amount = Decimal(request.data.get('final_amount'))
        print(id, order_id, create_at, method, status_pay, final_amount)
        data = (id, order_id, create_at, method, status_pay, final_amount,)
        result = ConnectByProd(prod_name= 'add_payment', data= data)

        return JsonResponse({'message': result}, status= status.HTTP_200_OK)
    return JsonResponse({'message': 'Invalid request method'}, status=400)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_schedule(request):
    if request.method == 'POST':
        query = 'SELECT (COALESCE(MAX(id), 0) + 1) FROM shipping_schedule;'
        id = ConnectByExcu(query= query)
        id = id[0][0]
        
        order_id = request.data.get('order_id')
        schedule = request.data.get('schedule')
        now = datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        data = (id, order_id, time, schedule,)
        result = ConnectByProd(prod_name='add_ship_schedule', data= data)

        return JsonResponse({'message': result}, status= status.HTTP_200_OK)
    return Response({'message': 'Invalid request method'}, status=400)


    
# @api_view(['POST'])
# def add_product(request, shop_id):
#     token_data = request.token_data
#     categories_id = token_data['categories_id']
#     name = token_data['name']
#     description = token_data['description']
#     price = token_data['price']
#     brand = token_data['brand']
#     stock_quantity = token_data['stock_quantity']
#     quantity_sold = token_data['quantity_sold']

#     with connection.cursor() as cursor: 
#         cursor.callproc('add_product', [shop_id, categories_id, name, description, price, brand, stock_quantity, quantity_sold])
#         result = cursor.fetchall()

#     return Response({'message': result})

# @api_view(['PUT'])
# def modify_product(request, shop_id, product_id):
#     token_data = request.token_data
#     update_data = {}
#     #which info & data update?
#     for field in ['name', 'description', 'price', 'brand', 'stock_quantity', 'quantity_sold']:
#         if field in token_data:
#             update_data[field] = token_data[field]
    
#     try:
#         product = ProductInfomation.objects.get(id= product_id)
#         for field, value in update_data.items():
#             setattr(product, field, value)
#         product.save()
#         return Response({'message': 'Update successful'})
    
#     except UserInfomation.DoesNotExist:
#         return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

# # delete product from shop
# @api_view(['DELETE'])
# def delete_product(request, shop_id, product_id):
#     try:

#         product = ProductInfomation.objects.get(id= product_id, shop_id = shop_id)
#         product.delete()
#         return Response({'message': 'Product deleted successfully'}, status=204)
    
#     except product.DoesNotExist:
#         return Response({'error': 'Product not found'}, status=404)
#     except Exception as e:
#         return Response({'error': str(e)}, status=500)


# @api_view(['DELETE'])
# def delete_from_cart(request, user_id, product_id):
#     try:
#         cart = CartInfomation(user_id = user_id, product_id = product_id)
#         cart.delete()
#         return Response({'message': 'Product deleted successfully'}, status=204)
#     except cart.DoesNotExist:
#         return Response({'error': 'Product not found'}, status=404)
#     except Exception as e:
#         return Response({'error': str(e)}, status=500)




# #API get profile không cần dùng token vẫn get được
# @api_view(['GET'])
# def get_info(request,user_id):
#     # id = request.token_data['id']
#     query = "SELECT fullname, address, phone, birth, role FROM users WHERE id = %s;"
#     with connection.cursor() as cursor: 
#         cursor.execute(query, (user_id,))
#         result = cursor.fetchall()

#     if result:
#         fullname, address, phone, birth, role = result[0]
#         payload = {
#             'fullname': fullname,
#             'address': address,
#             'phone': phone,
#             'birth': birth,
#             'role': role,
#         }

#         return Response({'data': payload})
#     return Response({'error': 'get info fail'}, status=status.HTTP_404_NOT_FOUND)


# # API update profile. Profile của người nào người đó update
# @api_view(['PUT'])
# def update_info(request,user_id):
#     #get data from request
#     data_token = request.token_data
#     update_data = {}
#     #which info & data update?
#     for field in ['password', 'fullname', 'address', 'birth', 'avatar', 'gender', 'phone', 'email', 'role']:
#         if field in data_token:
#             update_data[field] = data_token[field]

#     #check 
#     try:
#         # get object from database
#         # user_id = data_token['user_id']
#         user = UserInfomation.objects.get(id=user_id)
#         # update new info to postgres
#         for field, value in update_data.items():
#             setattr(user, field, value)
#         user.save()

#         return Response({'message': 'Update successful'})
#     except UserInfomation.DoesNotExist:
#         return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
# # modify shipping carts
# @api_view(['PUT'])
# def modify_cart(request, user_id, product_id):
#     data_token = request.token_data
#     new_quantity = data_token['new_quantity']
#     try:
#         product = CartInfomation(user_id = user_id, product_id = product_id)
#         setattr(product, 'new_quantity', new_quantity)
#         product.save()
#         return Response({'message': "successful!"}, status=status.HTTP_200_OK)
        
#     except CartInfomation.DoesNotExist:
#         return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
# # get all order of user
# @api_view(['GET'])
# def orders(request, user_id):
#     query = 'SELECT id, create_at, status, total_cost FROM orders WHERE user_id = %s;'
#     with connection.cursor() as cursor:
#         cursor.execute(query, (user_id,))
#         result = cursor.fetchall()

#     if result:
#         try:
#             id, create_at, status_order, total_cost = result[0]
#             payload = {
#                 'id': id,
#                 'create_at': create_at,
#                 'status': status_order,
#                 'total_cost': total_cost
#             }
#             token = jwt.encode(payload=payload, key='shopee_app', algorithm='HS256')
#             return Response({'data': token}, status=status.HTTP_200_OK)
#         except:
#             return Response({'message': 'fail'}, status= status.HTTP_404_NOT_FOUND)
#     else:
#         return Response({'error': 'error'}, status= status.HTTP_404_NOT_FOUND)
    

#     with connection.cursor() as cursor:
#         cursor.callproc()

# # add_order
# @api_view(['POST'])
# def add_order(request, user_id):
#     token_data = request.data
#     product_id = token_data['product_id']
#     quantity = token_data['quantity']
#     price  = token_data['price']
#     with connection.cursor() as cursor:
#         cursor.callproc('add_to_order', [user_id, product_id, quantity, price])
#         result = cursor.fetchall()
    
#     return Response({'message': result})

# @api_view(['DELETE'])
# def cancel_order(request, user_id): 

#     token_data = request.data
#     order_id = token_data['order_id']

#     try:

#         order = orders.objects.get(id= order_id, user_id = user_id)
#         order.delete()

#         detail = OrderDetail.object.get(order_id = order_id)
#         detail.delete()

#         return Response({'message': 'Order deleted successfully'}, status=204)
    
#     except order.DoesNotExist:
#         return Response({'error': 'order not found'}, status=404)
#     except detail.DoesNotExist:
#         return Response({'error': 'order detail not found'}, status=404)
    
# class UserRegisterView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
#             user = serializer.save()
            
#             return JsonResponse({
#                 'message': 'Register successful!'
#             }, status=status.HTTP_201_CREATED)

#         else:
#             return JsonResponse({
#                 'error_message': 'This email has already exist!',
#                 'errors_code': 400,
#             }, status=status.HTTP_400_BAD_REQUEST)