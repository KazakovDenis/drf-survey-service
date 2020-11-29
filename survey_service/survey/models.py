from datetime import date
from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


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
    survey = models.ForeignKey(
        Scheme,
        verbose_name=_('опрос'),
        related_name='questions',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('вопрос')
        verbose_name_plural = _('вопросы')
        unique_together = ('survey', 'text')

    def __str__(self):
        return self.text


class Participant(models.Model):
    """Участник опроса"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    full_name = models.TextField(_('полное имя'))

    class Meta:
        verbose_name = _('участник опроса')
        verbose_name_plural = _('участники опроса')


class Answer(models.Model):
    """Ответ на вопрос"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    participant = models.ForeignKey(
        Participant,
        verbose_name=_('участник опроса'),
        related_name='answers',
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        Question,
        verbose_name=_('вопрос'),
        related_name='answers',
        on_delete=models.CASCADE,
    )
    content = models.TextField(_('содержание ответа'))

    class Meta:
        verbose_name = _('ответ')
        verbose_name_plural = _('ответы')
        unique_together = ('participant', 'question')
