from dataclasses import dataclass as _dataclass, field as _field
from datetime import date as _date, timedelta as _td
from random import sample as _sample
from string import printable as _printable
from typing import Any

from rest_framework.reverse import reverse as _reverse


_today = _date.today()
TODAY = _today.strftime('%Y-%m-%d')
YESTERDAY = (_today - _td(days=1)).strftime('%Y-%m-%d')
TOMORROW = (_today + _td(days=1)).strftime('%Y-%m-%d')

USERNAME = 'test_user'
EMAIL = 'test@email.com'
PASSWORD = 'sup3rs3cr3tp@ssw0rd'
CREDENTIALS = {'username': USERNAME, 'password': PASSWORD}
CONTENT_TYPE = 'application/json'


class URL:
    GET_TOKEN = _reverse('get-token')
    VERSIONS = _reverse('api-versions-list')
    # V1_ROOT = resolve('/api/v1/')
    V1_DOC = _reverse('api-v1-doc')
    SCHEMES = _reverse('scheme-list')
    scheme = lambda uuid: _reverse('scheme-detail', kwargs={'pk': uuid})
    take_survey = lambda uuid: _reverse('scheme-take', kwargs={'pk': uuid})
    PARTICIPANTS = _reverse('participant-list')
    participant = lambda p_id: _reverse('participant-detail', kwargs={'pk': p_id})
    SURVEYS = _reverse('survey-list')
    survey = lambda p_id: _reverse('survey-detail', kwargs={'pk': p_id})


@_dataclass
class Case:
    name: str
    code: int
    data: dict
    response: Any = _field(default=None)


def random_str(length=10):
    return ''.join(_sample(_printable, length))
