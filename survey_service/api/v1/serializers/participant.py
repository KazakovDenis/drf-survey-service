from django.core.exceptions import ObjectDoesNotExist
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

        answers = []
        for q in scheme['questions']:
            answer = self._get_answer(q['id'])
            answers.append({
                    'id': answer['id'],
                    'question': q['text'],
                    'answer_type': q['answer_type'],
                    'answer_options': self._get_options(q['id']),
                    'answer': answer['content']
            })

        ret.update({
            'name': scheme['name'],
            'description': scheme['description'],
            'date_from': scheme['date_from'],
            'date_to': scheme['date_to'],
            'answers': answers,
        })
        return ret

    def _get_options(self, question_id):
        """Получить варианты ответов"""
        queryset = AnswerOption.objects.prefetch_related('question').filter(
            question__id=question_id,
        )
        options = [AnswerOptionSerializer(option).data for option in queryset]
        return options

    def _get_answer(self, question_id):
        """Получить сохранённый ответ участника"""
        question = Question.objects.get(pk=question_id)
        try:
            aq = AnswerQuestion.objects.prefetch_related('answer').get(
                question=question,
                answer__survey_answer__survey=self.instance
            )
            answer = aq.answer
        except ObjectDoesNotExist:
            answer = Answer.objects.create()
            AnswerQuestion.objects.create(answer=answer, question=question)
            SurveyAnswer.objects.create(survey=self.instance, answer=answer)

        return AnswerSerializer(answer).data

    class Meta:
        model = Survey
        fields = ['id', 'url', 'participant', 'scheme']


class ParticipantListSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор списка моделей участников опроса"""
    class Meta:
        model = Participant
        fields = ['id', 'url', 'full_name']


class ParticipantDetailSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор моделей участников опроса"""
    results = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='survey-detail'
    )

    class Meta:
        model = Participant
        fields = ['id', 'url', 'full_name', 'results']
