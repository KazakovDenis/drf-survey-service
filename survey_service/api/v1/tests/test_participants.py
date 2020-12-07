from json import dumps

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from survey import models
from .common import *


class ParticipantTest(APITestCase):
    """Проверка работы с участниками"""

    participant = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user_model = get_user_model()
        user_model.objects.create_superuser(email=EMAIL, **CREDENTIALS)
        cls.participant = models.Participant.objects.create()

    def tearDown(self):
        self.client.logout()

    def test_get_participant_list(self):
        """Проверка получения списка участников"""
        self.client.login(**CREDENTIALS)
        response = self.client.get(URL.PARTICIPANTS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        participants = response.data.get('results', [])
        participant_id = self.participant.id
        result = list(
            filter(lambda item: item['id'] == participant_id, participants)
        )
        self.assertEqual(len(result), 1)

    def test_get_participant(self):
        """Проверка просмотра информации об участнике"""
        url = URL.participant(self.participant.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_participant(self):
        """Проверка изменения информации об участнике"""
        self.client.login(**CREDENTIALS)
        url = URL.participant(self.participant.id)
        full_name = random_str()
        data = {'full_name': full_name}
        response = self.client.patch(url, data=dumps(data), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], full_name)
