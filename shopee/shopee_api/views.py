from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from .models import TokenInfomation
import jwt

# create user
@api_view(['POST'])
def signup(request):
    # 
    token_data = request.token_data
    name = token_data['name']
    password = token_data['password']
    email = token_data['email']
    phone = token_data['phone']

    # call function PostgreSQL
    with connection.cursor() as cursor:
        cursor.callproc('create_account', [name, password, email, phone])
        result = cursor.fetchone()[0]

    # Trả về kết quả dưới dạng JSON
    return Response({'message': result})


#API Login trả về token một số thông tin cô bản của user
@api_view(['POST'])
def login(request):
    token_data = request.token_data
    username = token_data['username']
    password = token_data['password']

    #call function on Postgres
    with connection.cursor() as cursor:
        cursor.callproc('login',[username,password,])
        result = cursor.fetchall()

    if result:
        info_data = result[0]
        id, fullname, address, phone, birth, role = info_data
        # create distionnary
        payload = {
            'id': str(id),
            'fullname': fullname,
            'address': address,
            'phone': phone,
            'birth': birth,
            'role': role,
        }
        token = jwt.encode(payload=payload, key= 'shopee_app', algorithm='HS256')

        return Response(token)
    return Response({'error':'login fail!'}, status=404)


#API get profile không cần dùng token vẫn get được
@api_view(['GET'])
def get_info(request):
    id = request.token_data['id']
    query = "SELECT fullname, address, phone, birth, role FROM users WHERE id = %s;"
    with connection.cursor() as cursor: 
        cursor.execute(query, (id,))
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
    return Response({'error': 'get info fail'}, status=404)


# API update profile. Profile của người nào người đó update
@api_view(['PUT'])
def update_info(request):
    #get data from request
    data_token = request.token_data
    update_data = {}

    #which info & data update?
    for field in ['password', 'fullname', 'address', 'birth', 'avatar', 'gender', 'phone', 'email', 'role']:
        if field in data_token:
            update_data[field] = data_token[field]

    #check 
    try:
        # get object from database
        user_id = data_token['user_id']
        user = TokenInfomation.objects.get(id=user_id)
        # update new info to postgres
        for field, value in update_data.items():
            setattr(user, field, value)
        user.save()

        return Response({'message': 'Update successful'})
    except TokenInfomation.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)