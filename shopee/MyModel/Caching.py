from django.core.cache import cache

'''trong trường hợp có dữ liệu ở bộ nhớ cache thì nó sẽ lấy dữ liệu ở phái Cache
còn không thì nó sẽ lấy data từ đầu vào của hàm và thêm vào cache đó và sau đó get data từ cache để biết rằng data đó đã được lưu ở cache'''
def Caching(key, data = None, timeout = 60):
    if cache.get(key= key):
        result = cache.get(key= key)
    else:
        cache.set(key= key, value= data, timeout= timeout)
        result = cache.get(key= key)
    return result