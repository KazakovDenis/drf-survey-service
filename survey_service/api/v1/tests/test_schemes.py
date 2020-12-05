from json import dumps

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .common import *


class SchemeTest(APITestCase):

    content_type = 'application/json'
    credentials = {
        'username': 'test_user',
        'email': 'test@email.com',
        'password': 'sup3rs3cr3tp@ssw0rd',
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user_model = get_user_model()
        user_model.objects.create_superuser(**cls.credentials)

    def setUp(self):
        self.client.login(**self.credentials)

    def test_get_schemes(self):
        url = reverse('scheme-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_scheme(self):
        url = reverse('scheme-list')
        non_unique = random_str()

        test_data = [
            # positive
            Case('Minimal', 201, {'name': non_unique}),
            # todo: Case('Name exists', {'name': non_unique, 'date_from': TOMORROW, 'date_to': TOMORROW}, 201),
            Case(
                'Full', 201,
                {'name': random_str(), 'date_from': TODAY, 'date_to': TOMORROW, 'description': random_str()},
            ),
            Case(
                'With question', 201,
                {'name': random_str(), 'questions': [{'text': random_str()}]},
            ),

            # negative
            Case('Name exists at this day', 400, {'name': non_unique}),
            Case('"date_to" should not be earlier', 400, {'name': random_str(), 'date_to': YESTERDAY}),
            # todo:
            # Case(
            #     'No answer options', 400,
            #     {
            #         'name': random_str(),
            #         'questions': [{'text': random_str(), 'answer_type': 'SINGLE'}]
            #     }
            # ),
        ]

        for case in test_data:
            with self.subTest(msg=case.name):
                response = self.client.post(
                    url, data=dumps(case.data), content_type=self.content_type
                )
                self.assertEqual(response.status_code, case.code)
