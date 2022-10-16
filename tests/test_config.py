from datetime import datetime, date

import pytest
from pendulum.tz.timezone import Timezone

import easy_pysi as ez


@pytest.mark.ez_app(dotenv_path='test_config.env')
def test_config(ez_app):
    assert ez.config('FOO') == 'BAR'
    assert ez.config('FORTY_TWO', type=int) == 42
    assert ez.config('ANY_DATETIME', type=datetime) == datetime(2022, 9, 21, 11, 26, 58, tzinfo=Timezone('UTC'))
    assert ez.config('ANY_DATE', type=date) == date(2022, 9, 21)
    assert ez.config('ALWAYS_TRUE', type=bool) is True
    assert ez.config('ALWAYS_FALSE', type=bool) is False
