from rest_framework import serializers

from survey.models import *


class ParticipantListSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор списка моделей участников опроса"""
    # todo: пройденные опросы

    class Meta:
        model = Participant
        fields = ['id', 'url', 'full_name']
