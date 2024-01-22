import requests
from django.db import connection
from django.core.cache import cache

def CallRequest(base_url, endpoint, data, headers):
    url = f'{base_url}{endpoint}/'
    response = requests.post(url= url, data= data, headers= headers)
    if response.status_code == 200:
        result = response.json()
    else:
        result = f'Error {endpoint} - Status Code: {response.status_code}'
    return result

def ConnectByExcu(query, data = None):
    with connection.cursor() as cursor:
        cursor.execute(query, data)
        result = cursor.fetchall()
    return result

def ConnectByProd(prod_name, data = None):
    with connection.cursor() as cursor:
        cursor.callproc(prod_name, data)
        result = cursor.fetchall()
    return result

'''trong trường hợp có dữ liệu ở bộ nhớ cache thì nó sẽ lấy dữ liệu ở phái Cache
còn không thì nó sẽ lấy data từ đầu vào của hàm và thêm vào cache đó và sau đó get data từ cache để biết rằng data đó đã được lưu ở cache'''
def Caching(key, data = None, timeout = 60):
    if cache.get(key= key):
        result = cache.get(key= key)
        print('data from Cache')
    else:
        cache.set(key= key, value= data, timeout= timeout)
        result = cache.get(key= key)
        print('data from db')
    return result