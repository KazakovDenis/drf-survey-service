from typing import Iterable, List

from rest_framework import serializers

from survey.models import *


def validate_options(question: Question, options: list):
    """Валидатор вариантов ответа на вопрос

    :param question: экземпляр Question
    :param options: список вариантов ответа
    """
    if question.answer_type == 'TEXT':
        if options:
            raise serializers.ValidationError('There should not be any answer options for the type "TEXT"')
    else:
        if (not isinstance(options, list)) or (len(options) < 2):
            raise serializers.ValidationError('Options should be a list of two or more values')


class AnswerOptionSerializer(serializers.ModelSerializer):
    """Сериализатор модели варианта ответа на вопрос"""

    def to_representation(self, iterable):
        ret = super().to_representation(iterable)
        return ret['text']

    class Meta:
        model = AnswerOption
        fields = ['text']


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор модели вопроса"""
    id = serializers.UUIDField(required=False)
    text = serializers.CharField(required=False, max_length=255)
    answer_options = AnswerOptionSerializer(many=True, required=False)

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


class SchemeSerializerMixin:

    question_model = Question
    questions_field = 'scheme_question'
    view_field = 'questions'

    def create(self, validated_data: dict):
        """Создать опрос"""
        questions_data = validated_data.pop(self.view_field)
        instance = self.Meta.model.objects.create(**validated_data)
        self.add_questions(instance, questions_data)
        return instance

    def validate_date_to(self, value):
        """Валидировать дату окончания опроса"""
        if value < self.instance.date_from:
            raise serializers.ValidationError('The value of "date_to" should not be earlier than "date_from"')
        return value

    def add_questions(self, instance: Scheme, questions_data: Iterable[dict]):
        """Добавить вопросы к опросу"""
        to_create = []
        for question_data in questions_data:
            data = question_data['question']
            options = data.pop('answer_options', [])
            question = Question(**data)
            question.save()
            self.add_options(question, options)

            sq = SchemeQuestion(scheme=instance, question=question)
            to_create.append(sq)

        if to_create:
            SchemeQuestion.objects.bulk_create(to_create)

    @staticmethod
    def add_options(question: Question, options: List[dict]):
        """Добавить варианты ответов"""
        options_field = getattr(question, 'answer_options')
        current_options = options_field.all()
        if current_options:
            current_options.delete()

        validate_options(question, options)
        to_create = []
        for v in options:
            instance = AnswerOption(**v)
            instance.question = question
            to_create.append(instance)

        if to_create:
            instances = AnswerOption.objects.bulk_create(to_create)
            options_field.set(instances)

    def delete_questions(self, questions_data: Iterable[dict]):
        """Удалить вопросы из опроса"""
        if questions_data:
            questions_ids = [i['question']['id'] for i in questions_data]
            self.question_model.objects.filter(id__in=questions_ids).delete()

    def update_questions(self, questions_data: Iterable[dict]):
        """Удалить вопросы из опроса"""
        to_update, fields = [], []
        for data in questions_data:
            question_data = data['question']
            question = self.question_model.objects.select_for_update().get(id=question_data['id'])
            serializer = QuestionSerializer(data=question_data)
            if serializer.is_valid(raise_exception=True):
                for field, value in serializer.validated_data.items():
                    if field == 'id':
                        continue
                    elif field == 'answer_options':
                        self.add_options(question, value)
                    else:
                        setattr(question, field, value)
                        fields.append(field)
                to_update.append(question)

        if to_update and fields:
            self.question_model.objects.bulk_update(to_update, fields=fields)

    def update_scheme_with_questions(self, instance: Scheme, questions_data: Iterable[dict]):
        """Обновить вопросы опроса"""
        data_to_delete = filter(
                lambda item: tuple(item['question'].keys()) == ('id',), questions_data
        )
        self.delete_questions(data_to_delete)

        def get_updating(item):
            keys = tuple(item['question'].keys())
            return 'id' in keys and keys != ('id',)

        data_to_update = filter(get_updating, questions_data)
        self.update_questions(data_to_update)

        new_data = filter(lambda item: item['question'].get('id') is None, questions_data)
        self.add_questions(instance, new_data)


class SchemeListSerializer(serializers.HyperlinkedModelSerializer, SchemeSerializerMixin):
    """Сериализатор списка моделей опроса"""

    class Meta:
        model = Scheme
        fields = ['id', 'url', 'name', 'description', 'date_from', 'date_to']


class SchemeSerializer(serializers.HyperlinkedModelSerializer, SchemeSerializerMixin):
    """Сериализатор модели опроса"""
    scheme_question = SchemeQuestionSerializer(many=True)

    def update(self, instance, validated_data):
        questions_data = validated_data.pop(self.questions_field, [])
        if questions_data:
            self.update_scheme_with_questions(instance, questions_data)
        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, iterable):
        ret = super().to_representation(iterable)
        ret[self.view_field] = ret.pop(self.questions_field)
        return ret

    class Meta:
        model = Scheme
        fields = ['id', 'url', 'name', 'description', 'date_from', 'date_to', 'scheme_question']
