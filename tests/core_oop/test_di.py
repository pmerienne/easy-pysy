from typing import ClassVar

from easy_pysy.core_oop.app import EzApp
from easy_pysy.core_oop.component import Component, Singleton


def test_inject_dependencies():
    class Heater(Component):
        power: float = 100

    class Machina(Singleton):
        heater: Heater

    app = EzApp(components=[Machina, Heater])
    app.start()

    machina = app.get(Machina)
    assert machina is not None and machina.heater is not None
    assert machina.heater.power == 100


def test_select_dependencies_according_to_env():
    class Google(Component):
        def search(self, query: str):
            raise NotImplementedError("Lol Protocol !")

    class GoogleProd(Google):
        profile: ClassVar[str] = 'prod'

        def search(self, query: str):
            return f'Prod: {query}'

    class GoogleTest(Google):
        profile: ClassVar[str] = 'test'

        def search(self, query: str):
            return f'Test: {query}'

    app = EzApp(components=[GoogleProd, GoogleTest])
    app.start()

    google = app.get(Google)
    assert google.search('Hello') == 'Test: Hello'



