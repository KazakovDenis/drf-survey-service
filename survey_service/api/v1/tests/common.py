from dataclasses import dataclass as _dataclass, field as _field
from datetime import date as _date, timedelta as _td
from random import sample as _sample
from string import printable as _printable


_today = _date.today()
TODAY = _today.strftime('%Y-%m-%d')
YESTERDAY = (_today - _td(days=1)).strftime('%Y-%m-%d')
TOMORROW = (_today + _td(days=1)).strftime('%Y-%m-%d')

USERNAME = 'test_user'
EMAIL = 'test@email.com'
PASSWORD = 'sup3rs3cr3tp@ssw0rd'
CREDENTIALS = {'username': USERNAME, 'password': PASSWORD}
CONTENT_TYPE = 'application/json'


@_dataclass
class Case:
    name: str
    code: int
    data: dict
    response: dict = _field(default=None)


def random_str(length=10):
    return ''.join(_sample(_printable, length))
