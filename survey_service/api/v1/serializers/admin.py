from django.db import transaction
from rest_framework import serializers

from survey.models import Scheme, Question, Answer


class SurveySerializerMixin:

    question_model = Question

    def add_questions(self, instance, questions_data):
        """Добавить вопросы к опросу"""
        self.question_model.objects.bulk_create(
            [Question(survey=instance, **q) for q in questions_data]
        )

    def update_questions(self, instance, questions_data):
        """Обновить вопросы опроса"""
        with transaction.atomic():
            survey_questions = self.question_model.objects.filter(survey=instance)
            survey_questions.delete()
            self.add_questions(instance, questions_data)


class SurveyQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор модели вопроса"""
    class Meta:
        model = Question
        fields = ['text', 'answer_type']


class SurveyListSerializer(serializers.HyperlinkedModelSerializer, SurveySerializerMixin):
    """Сериализатор списка моделей опроса"""
    questions = SurveyQuestionSerializer(many=True)

    def create(self, validated_data):
        """Создать опрос"""
        questions_data = validated_data.pop('questions')
        instance = self.Meta.model.objects.create(**validated_data)
        self.add_questions(instance, questions_data)
        return instance

    class Meta:
        model = Scheme
        fields = ['id', 'url', 'name', 'description', 'date_from', 'date_to', 'questions']


class SurveySerializer(SurveyListSerializer):
    """Сериализатор модели опроса"""

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions')
        self.update_questions(instance, questions_data)
        instance = super().update(instance, validated_data)
        return instance


class SurveyAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор модели ответа"""
    class Meta:
        model = Answer
        fields = ['content']
