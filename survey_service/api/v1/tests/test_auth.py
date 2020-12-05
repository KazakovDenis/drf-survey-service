from base64 import b64encode

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from survey.models import Scheme
from .common import *


class AuthTest(APITestCase):
    """Проверка аутентификации"""

    token = scheme = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        model = get_user_model()
        user = model.objects.create_superuser(email=EMAIL, **CREDENTIALS)
        cls.token = user.auth_token
        cls.scheme = Scheme.objects.create(name=random_str())

    def tearDown(self):
        self.client.credentials()
        self.client.logout()

    def test_basic_auth(self):
        """Проверка доступа по HTTP Basic Authentication"""
        url = URL.SCHEMES
        user_pass = f'{USERNAME}:{PASSWORD}'.encode()
        encoded = b64encode(user_pass).decode()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Basic {encoded}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_token(self):
        """Проверка получения токена по имени пользователя и паролю"""
        url = URL.GET_TOKEN
        response = self.client.post(url, data=CREDENTIALS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_token_auth(self):
        """Проверка доступа по токену"""
        url = URL.SCHEMES
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_public(self):
        """Проверка доступа к открытым endpoint"""
        public = (
            URL.VERSIONS, URL.V1_DOC, URL.SURVEYS
        )
        # todo: URL.V1_ROOT
        for url in public:
            with self.subTest(url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = URL.take_survey(self.scheme.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_private(self):
        """Проверка доступа к закрытым endpoint"""
        private = (
            URL.SCHEMES, URL.PARTICIPANTS, URL.scheme(self.scheme.id)
        )

        for url in private:
            with self.subTest(url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
