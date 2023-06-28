from datetime import datetime, date

from pendulum.tz.timezone import Timezone
from pydantic import BaseSettings, Field

from easy_pysy import EzApp, Component, EnvField


def test_env_field():
    class ChatGPTClient(Component):
        foo: str = EnvField()
        magic_number: int = EnvField(env='FORTY_TWO')
        any_datetime: datetime = EnvField()
        any_date: date = EnvField()
        always_true: bool = EnvField()
        always_false: bool = EnvField()

    app = EzApp(components=[ChatGPTClient])
    app.start()

    client = app.get(ChatGPTClient)

    assert client.foo == 'BAR'
    assert client.magic_number == 42
    assert client.any_datetime == datetime(2022, 9, 21, 11, 26, 58, tzinfo=Timezone('UTC'))
    assert client.any_date == date(2022, 9, 21)
    assert client.always_true is True
    assert client.always_false is False


def test_pydantic_settings():
    class ChatGPTSettings(Component, BaseSettings):
        foo: str = Field()
        magic_number: int = Field(env='FORTY_TWO')
        any_datetime: datetime = Field()
        any_date: date = Field()
        always_true: bool = Field()
        always_false: bool = Field()

    app = EzApp(components=[ChatGPTSettings])
    app.start()

    client = app.get(ChatGPTSettings)

    assert client.foo == 'BAR'
    assert client.magic_number == 42
    assert client.any_datetime == datetime(2022, 9, 21, 11, 26, 58, tzinfo=Timezone('UTC'))
    assert client.any_date == date(2022, 9, 21)
    assert client.always_true is True
    assert client.always_false is False
