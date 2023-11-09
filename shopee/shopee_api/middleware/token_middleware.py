from django.http import HttpResponseForbidden
import jwt

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.GET.get('token')  # Trích xuất token từ URL 
        if token:
            try:
                decoded_payload = jwt.decode(token, key='shopee_app', algorithm='HS256')
                print(decoded_payload)
                if decoded_payload:
                    request.token_data = decoded_payload
                else:
                    return HttpResponseForbidden("Token không hợp lệ")
            except jwt.DecodeError:
                return HttpResponseForbidden("Token không hợp lệ")
        response = self.get_response(request)
        return response