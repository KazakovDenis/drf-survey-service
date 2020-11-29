from django.db import transaction
from rest_framework import serializers

from survey.models import *


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор модели вопроса"""
    class Meta:
        model = Question
        fields = ['text', 'answer_type']


class SchemeQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор модели связи схемы и вопроса"""
    question = QuestionSerializer()

    def to_representation(self, iterable):
        ret = super().to_representation(iterable)
        return ret['question']

    class Meta:
        model = SchemeQuestion
        fields = ['question']


class SurveySerializerMixin:

    question_model = Question

    def create(self, validated_data):
        """Создать опрос"""
        questions_data = validated_data.pop('questions')
        instance = self.Meta.model.objects.create(**validated_data)
        self.add_questions(instance, questions_data)
        return instance

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

    class Meta:
        model = Scheme
        fields = ['id', 'url', 'name', 'description', 'date_from', 'date_to', 'scheme_question']


class SchemeListSerializer(serializers.HyperlinkedModelSerializer, SurveySerializerMixin):
    """Сериализатор списка моделей опроса"""
    scheme_question = SchemeQuestionSerializer(many=True)

    def to_representation(self, iterable):
        ret = super().to_representation(iterable)
        ret.pop('scheme_question')
        return ret


class SchemeSerializer(serializers.HyperlinkedModelSerializer, SurveySerializerMixin):
    """Сериализатор модели опроса"""
    scheme_question = SchemeQuestionSerializer(many=True)

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions')
        self.update_questions(instance, questions_data)
        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, iterable):
        ret = super().to_representation(iterable)
        ret['questions'] = ret.pop('scheme_question')
        return ret


class SurveyListSerializer(serializers.ModelSerializer):
    """Сериализатор списка результатов опросов"""
    class Meta:
        model = Survey
        fields = ['id', 'scheme']


class SurveySerializer(SurveyListSerializer):
    """Сериализатор модели результата опроса"""
