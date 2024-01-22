from django.test import TestCase
from .models import CustomUser
from django.test.client import RequestFactory
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth import authenticate, login
from .middleware.middleware import BasicAuthMidleware, TokemAuthentication, CookieAuthentication
from rest_framework.authtoken.models import Token
from django.test.client import RequestFactory

from codecs import encode
from base64 import b64encode




# class AuthenticationTests(TestCase):
#     def setUp(self):
#         # Tạo một user để sử dụng trong test
#         self.user = CustomUser.objects.create_user(username='user3', password='pass3')
#         self.token = Token.objects.create(user=self.user)
#         self.factory = RequestFactory()

#     def test_basic_auth_middleware(self):
#         authorization_header = 'Basic {}'.format(b64encode('{}:{}'.format(self.user.username, 'pass3').encode('utf-8')).decode('utf-8').strip())
#         request = self.factory.get('/')
#         request.META['HTTP_AUTHORIZATION'] = authorization_header

#         # Sử dụng middleware
#         basic_auth_middleware = BasicAuthMidleware(get_response=lambda x: None)
#         basic_auth_middleware(request)
#         print(basic_auth_middleware)

        # Kiểm tra xem user đã được thêm vào request hay không
        # self.assertEqual(request.user, self.user)

    # def test_token_authentication_middleware(self):
    #     # Tạo một request giả mạo với thông tin token
    #     request = self.factory.get('/')
    #     request.GET['token'] = self.token.key

    #     # Sử dụng middleware
    #     token_auth_middleware = TokemAuthentication(get_response=lambda x: None)
    #     token_auth_middleware(request)

    #     # Kiểm tra xem user đã được thêm vào request hay không
    #     self.assertEqual(request.user, self.user)

    # def test_cookie_authentication_middleware(self):
    #     # Tạo một request giả mạo với thông tin cookie
    #     request = self.factory.get('/')
    #     request.COOKIES['sessionid'] = 'your_session_id'  # Thay thế bằng session ID thực tế của bạn

    #     # Sử dụng middleware
    #     cookie_auth_middleware = CookieAuthentication(get_response=lambda x: None)
    #     cookie_auth_middleware(request)