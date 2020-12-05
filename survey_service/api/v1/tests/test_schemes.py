from json import dumps

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from survey.models import Scheme
from .common import *


class SchemeTest(APITestCase):
    """Проверка работы со схемами"""

    scheme = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user_model = get_user_model()
        user_model.objects.create_superuser(email=EMAIL, **CREDENTIALS)
        cls.scheme = Scheme.objects.create(name=random_str())

    def setUp(self):
        self.client.login(**CREDENTIALS)

    def test_get_scheme_list(self):
        """Проверка получения списка схем"""
        response = self.client.get(URL.SCHEMES)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        schemes = response.data.get('results', [])
        scheme_id = str(self.scheme.id)
        scheme_ids = list(
            filter(lambda item: item['id'] == scheme_id, schemes)
        )
        self.assertEqual(len(scheme_ids), 1)

    def test_get_scheme(self):
        """Проверка получения информации о схеме"""
        url = URL.scheme(self.scheme.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.scheme.name)

    def test_create_scheme(self):
        """Проверка создания схемы"""
        non_unique = random_str()

        test_data = [
            # positive
            Case('Minimal', 201, {'name': non_unique}),
            # todo: Case('Name exists', {'name': non_unique, 'date_from': TOMORROW, 'date_to': TOMORROW}, 201),
            Case(
                'Full survey info', 201,
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
                    URL.SCHEMES, data=dumps(case.data), content_type=CONTENT_TYPE
                )
                self.assertEqual(response.status_code, case.code)

    # todo
    def t_edit_scheme(self):
        """Проверка изменения схемы"""
        # todo: add, edit, delete questions
        pass

    def test_delete_scheme(self):
        """Проверка удаления схемы"""
        scheme = Scheme.objects.create(name=random_str())
        url = URL.scheme(scheme.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
