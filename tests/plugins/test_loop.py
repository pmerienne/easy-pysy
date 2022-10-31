import time

import easy_pysy as ez
from easy_pysy.core.app import AppState

TIMES = {}
STATE = None


@ez.loop(every_ms=200)
def increase():
    ez.info(f'Increase')
    TIMES[time.time()] = 42
    time.sleep(0.100)  # Really useful to ensure intervals are not shifting


@ez.loop(every_ms=200, stop_app_on_error=True, auto_start=False)
def will_raise_and_stop_app():
    ez.info('I will raise and stop')
    raise RuntimeError()


@ez.loop(every_ms=200, stop_app_on_error=False, auto_start=False)
def will_raise_and_not_stop_app():
    ez.info('I will raise but not stop')
    raise RuntimeError()


def test_loop_should_call_every_ms(ez_app):
    TIMES.clear()
    time.sleep(1.010)
    assert len(TIMES) == 5


def test_stop_start_loop(ez_app):
    loop = ez.get_loop(increase)
    loop.stop()
    TIMES.clear()

    time.sleep(1.0)
    assert len(TIMES) == 0

    loop.start()
    time.sleep(1.010)
    assert len(TIMES) == 5


def test_should_stop_app_on_error(ez_app):
    loop = ez.get_loop(will_raise_and_stop_app)
    loop.start()
    time.sleep(0.3)

    assert ez.context.state == AppState.STOPPED


def test_should_not_stop_app_on_error(ez_app):
    loop = ez.get_loop(will_raise_and_not_stop_app)
    loop.start()
    time.sleep(0.3)

    assert ez.context.state == AppState.STARTED
