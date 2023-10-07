import time

from pydantic import Field, BaseModel

from easy_pysy import EzApp, Service, loop, Singleton, uuid


class ImUnique(Singleton):
    uuid: str = Field(default_factory=uuid)


def test_provided_instances():
    the_only_one = ImUnique()
    with EzApp(providers={ImUnique: the_only_one}) as app:
        candidate = app.container.get(ImUnique)
        assert candidate == the_only_one
