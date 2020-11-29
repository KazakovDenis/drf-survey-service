from datetime import date
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class Participant(models.Model):
    """Участник опроса"""
    full_name = models.TextField(_('полное имя'))

    class Meta:
        verbose_name = _('участник опроса')
        verbose_name_plural = _('участники опроса')

    def __str__(self):
        return f'Участник №{self.id}'


class Scheme(models.Model):
    """Опрос"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    name = models.CharField(_('название'), max_length=255)
    description = models.TextField(_('описание'), blank=True)
    date_from = models.DateField(_('дата начала'), default=date.today, editable=False)
    date_to = models.DateField(_('дата окончания'), default=date.today)

    class Meta:
        verbose_name = _('опрос')
        verbose_name_plural = _('опросы')
        unique_together = ('name', 'date_from')
        ordering = ['-date_from']

    def __str__(self):
        return self.name


class Survey(models.Model):
    """Пройденный опрос"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    scheme = models.ForeignKey(
        Scheme,
        verbose_name=_('опрос'),
        related_name='results',
        on_delete=models.CASCADE,
    )
    participant = models.ForeignKey(
        Participant,
        verbose_name=_('участник'),
        related_name='results',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('пройденный опрос')
        verbose_name_plural = _('пройденные опросы')
        ordering = ['-scheme']

    def __str__(self):
        return f'{self.scheme.name} - {self.participant}'


class Question(models.Model):
    """Вопрос из опроса"""
    ANSWER_TYPES = (
        ('TEXT', _('ответ текстом')),
        ('SINGLE', _('ответ с выбором одного варианта')),
        ('MULTIPLE', _('ответ с выбором нескольких вариантов')),
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    text = models.CharField(_('текст вопроса'), max_length=255)
    answer_type = models.CharField(_('тип ответа'), choices=ANSWER_TYPES, default='TEXT', max_length=127)

    class Meta:
        verbose_name = _('вопрос')
        verbose_name_plural = _('вопросы')
        unique_together = ('survey', 'text')

    def __str__(self):
        return self.text


class SchemeQuestion(models.Model):
    """Связь вопросов с опросами"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    scheme = models.ForeignKey(
        Scheme,
        verbose_name=_('опрос'),
        related_name='scheme_question',
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        verbose_name=_('вопрос'),
        related_name='scheme_question',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('связь вопросов с опросами')
        verbose_name_plural = _('связи вопросов с опросами')
        unique_together = ('scheme', 'question')


class SurveyQuestion(models.Model):
    """Связь вопросов с пройденными опросами"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    survey = models.ForeignKey(
        Survey,
        verbose_name=_('пройденный опрос'),
        related_name='survey_question',
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        verbose_name=_('вопрос'),
        related_name='survey_question',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('связь вопросов с пройденными опросами')
        verbose_name_plural = _('связи вопросов с пройденными опросами')
        unique_together = ('survey', 'question')


class Answer(models.Model):
    """Ответ на вопрос"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    content = models.TextField(_('содержание ответа'))

    class Meta:
        verbose_name = _('ответ')
        verbose_name_plural = _('ответы')


class AnswerQuestion(models.Model):
    """Связь ответов с вопросами"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    answer = models.ForeignKey(
        Answer,
        verbose_name=_('ответ'),
        related_name='answer_question',
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        verbose_name=_('вопрос'),
        related_name='answer_question',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('связь ответов с вопросами')
        verbose_name_plural = _('связи ответов с вопросами')
        unique_together = ('answer', 'question')


class SurveyAnswer(models.Model):
    """Связь ответов с пройденными опросами"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    survey = models.ForeignKey(
        Survey,
        verbose_name=_('опрос'),
        related_name='survey_answer',
        on_delete=models.CASCADE,
    )
    answer = models.ForeignKey(
        Answer,
        verbose_name=_('ответ'),
        related_name='survey_answer',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('связь ответов с пройденными опросами')
        verbose_name_plural = _('связи ответов с пройденными опросами')
        unique_together = ('survey', 'answer')

