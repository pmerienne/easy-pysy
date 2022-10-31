from datetime import datetime, date

from pendulum.tz.timezone import Timezone

import easy_pysy as ez


def test_config(ez_app):
    assert ez.config('FOO') == 'BAR'
    assert ez.config('FORTY_TWO', config_type=int) == 42
    assert ez.config('ANY_DATETIME', config_type=datetime) == datetime(2022, 9, 21, 11, 26, 58, tzinfo=Timezone('UTC'))
    assert ez.config('ANY_DATE', config_type=date) == date(2022, 9, 21)
    assert ez.config('ALWAYS_TRUE', config_type=bool) is True
    assert ez.config('ALWAYS_FALSE', config_type=bool) is False
