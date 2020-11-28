from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class Survey(models.Model):
    """Опрос"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    name = models.CharField(_('название'), max_length=255)
    description = models.TextField(_('описание'), blank=True, null=True)
    created = models.DateTimeField(_('создан'), editable=False)

    class Meta:
        verbose_name = _('опрос')
        verbose_name_plural = _('опросы')

    def __str__(self):
        return self.name
