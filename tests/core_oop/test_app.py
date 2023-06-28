from easy_pysy.core_oop.app import EzApp
from easy_pysy.core_oop.component import Component, Singleton


def test_get_instance():
    class Heater(Component):
        power: float = 100

    app = EzApp(components=[Heater])
    app.start()

    first_heater = app.get(Heater)
    second_heater = app.get(Heater)

    assert first_heater.power == second_heater.power == 100
    first_heater.power = 33
    assert first_heater.power == 33
    assert second_heater.power == 100


def test_get_singleton_instance():
    class Heater(Singleton):
        power: float = 100

    app = EzApp(components=[Heater])
    app.start()

    first_heater = app.get(Heater)
    second_heater = app.get(Heater)

    assert first_heater.power == second_heater.power == 100
    first_heater.power = 33
    assert first_heater.power == second_heater.power == 33
