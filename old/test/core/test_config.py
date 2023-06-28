from datetime import datetime, date

from pendulum.tz.timezone import Timezone

import easy_pysy as ez


def test_config(ez_app):
    assert ez.env('FOO') == 'BAR'
    assert ez.env('FORTY_TWO', config_type=int) == 42
    assert ez.env('ANY_DATETIME', config_type=datetime) == datetime(2022, 9, 21, 11, 26, 58, tzinfo=Timezone('UTC'))
    assert ez.env('ANY_DATE', config_type=date) == date(2022, 9, 21)
    assert ez.env('ALWAYS_TRUE', config_type=bool) is True
    assert ez.env('ALWAYS_FALSE', config_type=bool) is False
