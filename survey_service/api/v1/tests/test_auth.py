from base64 import b64encode

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .common import *


class AuthTest(APITestCase):

    user = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        model = get_user_model()
        cls.user = model.objects.create_superuser(email=EMAIL, **CREDENTIALS)

    def tearDown(self):
        self.client.credentials()
        self.client.logout()

    def test_basic_auth(self):
        url = reverse('scheme-list')
        user_pass = f'{USERNAME}:{PASSWORD}'.encode()
        encoded = b64encode(user_pass).decode()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Basic {encoded}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_token(self):
        url = reverse('get-token')
        response = self.client.post(url, data=CREDENTIALS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_token_auth(self):
        url = reverse('scheme-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
