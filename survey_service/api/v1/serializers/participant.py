from rest_framework import serializers

from survey.models import *
from .admin import SchemeSerializer, QuestionSerializer


class AnswerSerializer(serializers.ModelSerializer):
    """Сериализатор моделей ответов участника"""
    class Meta:
        model = Answer
        fields = ['id', 'content']


class AnswerQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор модели связи схемы и вопроса"""
    answer = AnswerSerializer()
    question = QuestionSerializer()

    class Meta:
        model = AnswerQuestion
        fields = ['answer', 'question']


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
            'questions': [
                {
                    **q,
                    'choices': self._get_choices(q['id']),
                    'answer': self._get_answer(q['id'])
                }
                for q in scheme['questions']
            ],
        })
        return ret

    def _get_choices(self, question_id):
        """Получить варианты ответов"""
        return None

    def _get_answer(self, question_id):
        """Получить сохранённый ответ участника"""
        question = Question.objects.get(pk=question_id)
        AnswerQuestionSerializer(question=question)
        return None

    class Meta:
        model = Survey
        fields = ['id', 'url', 'participant', 'scheme']


class ParticipantListSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор списка моделей участников опроса"""
    results = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='survey-detail'
    )

    class Meta:
        model = Participant
        fields = ['id', 'url', 'full_name', 'results']
