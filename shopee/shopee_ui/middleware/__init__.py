from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTAuthentication:
    def __init__(self, get_respone):
        self.get_response = get_respone

    def __call__(self, request):
        jwt_auth = JWTAuthentication()
        user, _ =  jwt_auth.authentication(request)
        request.user = user
        return self.get_response(request)