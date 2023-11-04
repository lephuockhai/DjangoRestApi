from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .models import TokenInfomation
import jwt

@api_view(['GET'])
def get_info(request):
    user_id = 1
    query = "SELECT fullname, address, phone, birth, role FROM users WHERE id = %s;"

    with connection.cursor() as cursor: 
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
    if result:
        first_record = result[0]  # Lấy bản ghi đầu tiên từ danh sách
        fullname, address, phone, birth, role = first_record
        payload = {
            'fullname': fullname,
            'address': address,
            'phone': phone,
            'birth': birth,
            'role': role,
        }

        return Response({'data': payload})
    else:
        # 
        return Response({'message': 'get info fail'}, status=404)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Gọi hàm PostgreSQL
    with connection.cursor() as cursor:
        cursor.callproc('login', [username, password])
        result = cursor.fetchall()

    if result:
        # if login successful then continue
        first_record = result[0]  # Lấy bản ghi đầu tiên từ danh sách
        id, fullname, address, phone, birth, role = first_record

        # create distionnary
        payload = {
            'id': str(id),
            'fullname': fullname,
            'address': address,
            'phone': phone,
            'birth': birth,
            'role': role,
        }
        
        token = jwt.encode(payload=payload, key= str(id), algorithm='HS256')

        return Response({'message': 'Login successful', 'data': token})
    else:
        # Đăng nhập thất bại, trả về thông báo lỗi.
        return Response({'message': 'Login failed'})



@api_view(['POST'])
def create_account(request):
    # Lấy dữ liệu từ yêu cầu POST
    name = request.data.get('name')
    password = request.data.get('password')
    email = request.data.get('email')
    phone = request.data.get('phone')

    # Gọi hàm PostgreSQL
    with connection.cursor() as cursor:
        cursor.callproc('create_account', [name, password, email, phone])
        result = cursor.fetchone()[0]

    # Trả về kết quả dưới dạng JSON
    return Response({'message': result})

@api_view(['PUT'])
def update_info(request):
    # password = request.data.get('password')
    # fullname = request.data.get('fullname')
    # address = request.data.get('address')
    # birth = request.data.get('birth')
    # avatar = request.data.get('avatar')
    # gender = request.data.get('gender')
    # phone = request.data.get('phone')
    # email = request.data.get('email')
    # Lấy thông tin từ request data
    update_data = {}
    for field in ['password', 'fullname', 'address', 'birth', 'avatar', 'gender', 'phone', 'email']:
        if field in request.data:
            update_data[field] = request.data[field]

    # user_id for update info
    user_id = request.data.get('user_id')  

    try:
        # get object from database
        user = TokenInfomation.objects.get(id=user_id)

        # update new info to postgres
        for field, value in update_data.items():
            setattr(user, field, value)

        # save
        user.save()

        # 
        return Response({'message': 'Update successful'})
    except TokenInfomation.DoesNotExist:
        # 
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

