from django.db import transaction
from rest_framework import serializers

from survey.models import *


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


class SchemeListSerializer(serializers.HyperlinkedModelSerializer, SurveySerializerMixin):
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


class SchemeSerializer(SchemeListSerializer):
    """Сериализатор модели опроса"""

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions')
        self.update_questions(instance, questions_data)
        instance = super().update(instance, validated_data)
        return instance


class SurveyListSerializer(serializers.ModelSerializer):
    """Сериализатор списка результатов опросов"""
    class Meta:
        model = Survey
        fields = ['id', 'scheme.name', 'scheme.description', 'scheme.date_from', 'scheme.date_to']


class SurveySerializer(SurveyListSerializer):
    """Сериализатор модели результата опроса"""
