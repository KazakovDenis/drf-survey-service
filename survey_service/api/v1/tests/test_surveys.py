from json import dumps

from rest_framework import status
from rest_framework.test import APITestCase

from survey import models
from .common import *


class SurveyTest(APITestCase):
    """Проверка работы с опросами"""

    scheme = survey = question = participant = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.scheme = models.Scheme.objects.create(name=random_str())
        cls.participant = models.Participant.objects.create()
        cls.survey = models.Survey.objects.create(scheme=cls.scheme, participant=cls.participant)
        cls.question = models.Question.objects.create(text=random_str())
        models.SchemeQuestion.objects.create(scheme=cls.scheme, question=cls.question)

    def test_get_survey_list(self):
        """Проверка получения списка опросов"""
        response = self.client.get(URL.SURVEYS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        surveys = response.data.get('results', [])
        scheme_id = str(self.scheme.id)
        result = list(
            filter(lambda item: scheme_id in item['url'], surveys)
        )
        self.assertEqual(len(result), 1)

    def test_get_survey(self):
        """Проверка просмотра пройденного опроса"""
        url = URL.survey(self.survey.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.scheme.name)

    def test_take_survey(self):
        """Проверка возможности прохождения опроса"""
        # анонимно
        url = URL.take_survey(self.scheme.id)
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # участником, уже проходившим опросы
        participant_url = response.data['participant']
        participant_id = participant_url.rsplit('/')[-1]
        url = f'{url}?participant_id={participant_id}'
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['participant'], participant_url)

    def test_send_answers(self):
        """Проверка возможности отправки ответов"""
        # todo: positive + negative cases
        url = URL.survey(self.survey.id)
        response = self.client.get(url)
        answer_id = response.data['answers'][0]['id']

        answer = random_str()
        data = {'answers': [{'id': answer_id, 'answer': answer}]}
        response = self.client.patch(url, data=dumps(data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        resp_answer = response.data['answers'][0]['answer']
        self.assertEqual(resp_answer, answer)
