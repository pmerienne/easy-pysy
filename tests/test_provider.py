import sys

import pytest

import easy_pysy as ez
from tests.woofer import bar_woofer, foo_woofer, Woofer


@pytest.mark.ez_app(modules=[sys.modules[__name__], foo_woofer])
def test_provide(ez_app):
    woofer = ez.get(Woofer)
    assert woofer.say_woof() == 'Foo Woof'
    assert woofer != ez.get(Woofer)


@pytest.mark.ez_app(modules=[sys.modules[__name__], bar_woofer])
def test_provide_alternative_singleton(ez_app):
    woofer = ez.get(Woofer)
    assert woofer.say_woof() == 'Bar Woof'
    assert woofer == ez.get(Woofer)
