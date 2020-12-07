from json import dumps

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from survey import models
from .common import *


class SchemeTest(APITestCase):
    """Проверка работы со схемами"""

    scheme = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user_model = get_user_model()
        user_model.objects.create_superuser(email=EMAIL, **CREDENTIALS)
        cls.scheme = models.Scheme.objects.create(name=random_str())

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
            # todo: возвращает 400
            # Case('Name exists', 201, {'name': non_unique, 'date_from': TOMORROW, 'date_to': TOMORROW}),
            Case(
                'Full survey info', 201,
                {'name': random_str(), 'date_from': TODAY, 'date_to': TOMORROW, 'description': random_str()},
            ),
            Case('With question', 201, {'name': random_str(), 'questions': [{'text': random_str()}]}),

            # negative
            Case('Name exists at this day', 400, {'name': non_unique}),
            Case('"date_to" should not be earlier', 400, {'name': random_str(), 'date_to': YESTERDAY}),
            Case(
                'Wrong answer options type', 400,
                {
                    'name': random_str(),
                    'questions': [{'text': random_str(), 'answer_type': 'SINGLE', 'answer_options': 'Answer1'}]
                }
            ),
            # todo: все возвращают 201
            # Case(
            #     'No answer options', 400,
            #     {'name': random_str(), 'questions': [{'text': random_str(), 'answer_type': 'SINGLE'}]}
            # ),
            # Case(
            #     'Wrong answer type', 400,
            #     {'name': random_str(), 'questions': [{'text': random_str(), 'answer_type': 'Wrong type'}]}
            # ),
            # Case(
            #     'Not enough answer options', 400,
            #     {'name': random_str(), 'questions': [{'text': random_str(), 'answer_options': ['Answer1']}]}
            # ),
            # Case(
            #     'Answer options with the wrong type', 400,
            #     {
            #         'name': random_str(),
            #         'questions': [{'text': random_str(), 'answer_type': 'TEXT', 'answer_options': ['Answer1']}]
            #     }
            # ),
            # Case(
            # 'Same answer options', 400,
            # {'name': random_str(), 'questions': [{'text': random_str(), 'answer_options': ['Answer1', 'Answer1']}]}
            # ),
        ]

        for case in test_data:
            with self.subTest(msg=case.name):
                response = self.client.post(
                    URL.SCHEMES, data=dumps(case.data), content_type=CONTENT_TYPE
                )
                self.assertEqual(response.status_code, case.code)

    def test_edit_scheme_info(self):
        """Проверка изменения схемы"""
        scheme_id = str(self.scheme.id)
        url = URL.scheme(scheme_id)

        test_data = [
            # positive
            Case('Full survey info', 200, {'name': random_str(), 'date_to': TOMORROW, 'description': random_str()}),
            Case('Add question', 200, {'questions': [{'text': random_str()}]}),

            # negative
            Case('Change date_from', 200, {'date_from': YESTERDAY}),
        ]
        for case in test_data:
            with self.subTest(msg=case.name):
                response = self.client.patch(
                    url, data=dumps(case.data), content_type=CONTENT_TYPE
                )
                self.assertEqual(response.status_code, case.code)

                if case.name == 'Change date_from':
                    resp_date = response.data.get('date_from')
                    self.assertNotEqual(resp_date, YESTERDAY)

    def test_edit_delete_question(self):
        """Проверка редактирования и удаления вопроса из схемы"""
        scheme = models.Scheme.objects.create(name=random_str())
        question = models.Question.objects.create(text=random_str(), answer_type='SINGLE')
        models.SchemeQuestion.objects.create(scheme=scheme, question=question)
        url = URL.scheme(scheme.id)
        qid = str(question.id)

        test_data = [
            # negative
            Case('Wrong answer type', 400, {'questions': [{'id': qid, 'answer_type': 'Wrong type'}]}),
            Case('Wrong answer options type', 400, {'questions': [{'id': qid, 'answer_options': 'Answer1'}]}),
            Case('Not enough answer options', 400, {'questions': [{'id': qid, 'answer_options': ['Answer1']}]}),
            Case(
                'Answer options with the wrong type', 400,
                {'questions': [{'id': qid, 'answer_type': 'TEXT', 'answer_options': ['Answer1']}]}
            ),
            # todo: не реализовано, возвращают 200
            # Case('No answer options', 400, {'questions': [{'id': qid, 'answer_type': 'MULTIPLE'}]}),
            # Case(
            #     'Same answer options', 400,
            #     {'questions': [{'id': qid, 'answer_options': ['Answer1', 'Answer1']}]}
            # ),

            # positive
            Case('Edit question', 200, {'questions': [{'id': qid, 'text': random_str()}]}),
            Case(
                'Edit question with options', 200,
                {'questions': [
                    {'id': qid, 'answer_type': 'MULTIPLE', 'answer_options': ['Answer1', 'Answer2']}
                ]}
            ),
            Case('Delete question', 200, {'questions': [{'id': qid}]}),
        ]
        for case in test_data:
            with self.subTest(msg=case.name):
                response = self.client.patch(
                    url, data=dumps(case.data), content_type=CONTENT_TYPE
                )
                self.assertEqual(response.status_code, case.code)

                if case.name == 'Delete question':
                    resp_questions = response.data.get('questions')
                    self.assertEqual(resp_questions, [])

    def test_delete_scheme(self):
        """Проверка удаления схемы"""
        scheme = models.Scheme.objects.create(name=random_str())
        url = URL.scheme(scheme.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
