from typing import Union, Iterable
from uuid import UUID

from rest_framework import serializers

from survey.models import *


class AnswerOptionSerializer(serializers.ModelSerializer):
    """Сериализатор модели варианта ответа на вопрос"""

    def to_representation(self, iterable):
        ret = super().to_representation(iterable)
        return ret['text']

    class Meta:
        model = AnswerOption
        fields = ['text']


# todo: валидация вариантов ответов при answer_type != 'TEXT'
class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор модели вопроса"""
    answer_options = AnswerOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answer_type', 'answer_options']


class SchemeQuestionSerializer(serializers.ModelSerializer):
    """Сериализатор модели связи схемы и вопроса"""
    question = QuestionSerializer()

    def to_representation(self, iterable):
        ret = super().to_representation(iterable)
        return ret['question']

    class Meta:
        model = SchemeQuestion
        fields = ['question']


# todo: валидация дат (date_to >= date_from)
class SchemeSerializerMixin:

    question_model = Question

    def create(self, validated_data: dict):
        """Создать опрос"""
        questions_data = validated_data.pop('questions')
        instance = self.Meta.model.objects.create(**validated_data)
        self.add_questions(instance, questions_data)
        return instance

    def add_questions(self, instance: Scheme, questions_data: Iterable[dict]):
        """Добавить вопросы к опросу"""
        serialized_data = []
        for question_data in questions_data:
            serializer = QuestionSerializer(data=question_data)
            if serializer.is_valid(raise_exception=True):
                serialized_data.append(serializer.data)

        self.question_model.objects.bulk_create(
            [self.question_model(scheme=instance, **q) for q in serialized_data]
        )

    def delete_questions(self, questions_ids: Iterable[Union[UUID, str]]):
        """Удалить вопросы из опроса"""
        if questions_ids:
            self.question_model.objects.filter(id__in=questions_ids).delete()

    def update_questions(self, questions_data: Iterable[dict]):
        """Удалить вопросы из опроса"""
        to_update = []
        for question_data in questions_data:
            question = self.question_model.objects.select_for_update().get(id=question_data['id'])
            serializer = QuestionSerializer(data=question_data)
            if serializer.is_valid(raise_exception=True):
                for field, value in serializer.data:
                    setattr(question, field, value)
                to_update.append(question)

        self.question_model.objects.bulk_update(
            to_update, fields=['text', 'answer_type', 'answer_options']
        )

    def update_scheme_with_questions(self, instance: Scheme, questions_data: Iterable[dict]):
        """Обновить вопросы опроса"""
        all_data = set(questions_data)
        new_data = set(
            filter(lambda item: item.get('id') is None, all_data)
        )
        self.add_questions(instance, new_data)

        existing_data = all_data - new_data
        data_to_delete = set(filter(
                lambda item: tuple(item.keys()) == ('id',), existing_data
        ))

        data_to_update = existing_data - data_to_delete
        self.update_questions(data_to_update)


class SchemeListSerializer(serializers.HyperlinkedModelSerializer, SchemeSerializerMixin):
    """Сериализатор списка моделей опроса"""

    class Meta:
        model = Scheme
        fields = ['id', 'url', 'name', 'description', 'date_from', 'date_to']


class SchemeSerializer(serializers.HyperlinkedModelSerializer, SchemeSerializerMixin):
    """Сериализатор модели опроса"""
    scheme_question = SchemeQuestionSerializer(many=True)

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', [])
        if questions_data:
            self.update_scheme_with_questions(instance, questions_data)
        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, iterable):
        ret = super().to_representation(iterable)
        ret['questions'] = ret.pop('scheme_question')
        return ret

    class Meta:
        model = Scheme
        fields = ['id', 'url', 'name', 'description', 'date_from', 'date_to', 'scheme_question']
