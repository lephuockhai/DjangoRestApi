import jwt
from django.conf import settings
from shopee_api.models import CustomUser
from datetime import datetime, timedelta
class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lấy token từ cookie
        token = request.session.get('token')
        print('token middleware api: ',token)
        if token is not None:
            try:
                payload = jwt.decode(token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
                exp_time = datetime.utcfromtimestamp(payload['exp'])
                current_time = datetime.utcnow()

                if exp_time < current_time:
                    print("het han o server api")
                    request.token_expired = True
                else:
                    user_id = payload.get('user_id')
                    user = CustomUser.objects.get(pk=user_id)
                    request.user = user
                    
            except jwt.InvalidTokenError:
                request.invalid_token = True
        
        response = self.get_response(request)
        return response
