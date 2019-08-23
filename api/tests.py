import base64

from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token


# Basic Auth
class AuthTests(APITestCase):
    def setUp(self):
        self.username = 'admin'
        self.password = 'admin123'
        self.url = "/api/users/"
        self.user = User.objects.create_user(username=self.username, password=self.password)

        credentials = base64.b64encode(f'{self.username}:{self.password}'.encode('utf-8'))
        self.client.credentials(HTTP_AUTHORIZATION='Basic {}'.format(credentials.decode('utf-8')))

    def test_is_authenticated(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)


# Token Auth
class TokenAuthTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = "/api/users/"
        self.user = User.objects.create_user(
            username='admin',
            password='admin123')
        self.token = Token.objects.create(user=self.user)

    def test_token_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token))

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
