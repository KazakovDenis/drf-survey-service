from rest_framework import serializers

from survey.models import *
from .admin import SchemeSerializer


class ParticipantListSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор списка моделей участников опроса"""
    # todo: пройденные опросы

    class Meta:
        model = Participant
        fields = ['id', 'url', 'full_name']


class SurveyListSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор списка результатов опросов"""

    def to_representation(self, iterable):
        ret = super().to_representation(iterable)
        ret['url'] = ret['url'] + '/take'
        return ret

    class Meta:
        model = Scheme
        fields = ['url', 'name', 'description', 'date_from', 'date_to']


class SurveySerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор модели результата опроса"""
    scheme = SchemeSerializer()

    def to_representation(self, iterable):
        ret = super().to_representation(iterable)
        scheme = ret.pop('scheme')
        ret.update({
            'name': scheme['name'],
            'description': scheme['description'],
            'date_from': scheme['date_from'],
            'date_to': scheme['date_to'],
            'questions': scheme['questions'],
        })
        return ret

    class Meta:
        model = Survey
        fields = ['id', 'url', 'participant', 'scheme']
