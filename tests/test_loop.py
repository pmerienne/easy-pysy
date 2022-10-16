import time

import easy_pysi as ez
from easy_pysi.core import AppState
from easy_pysi.loop import LoopPlugin

TIMES = {}
STATE = None


@ez.loop(every_ms=200)
def increase():
    TIMES[time.time()] = 42


@ez.loop(every_ms=200, stop_app_on_error=True, auto_start=False)
def will_raise_and_stop_app():
    raise RuntimeError()


@ez.loop(every_ms=200, stop_app_on_error=False, auto_start=False)
def will_raise_and_not_stop_app():
    raise RuntimeError()


def test_loop_should_call_every_ms(ez_app):
    time.sleep(1.0)
    assert len(TIMES) == 5


def test_stop_start_loop(ez_app):
    last_time = len(TIMES)
    loop = ez.plugin(LoopPlugin).get_loop(increase)

    loop.stop()
    time.sleep(1.0)
    assert len(TIMES) == last_time

    loop.start()
    time.sleep(1.0)
    assert len(TIMES) == last_time + 5


def test_should_stop_app_on_error(ez_app):
    loop = ez.plugin(LoopPlugin).get_loop(will_raise_and_stop_app)
    loop.start()
    time.sleep(0.3)

    assert ez_app.state == AppState.STOPPED


def test_should_not_stop_app_on_error(ez_app):
    loop = ez.plugin(LoopPlugin).get_loop(will_raise_and_not_stop_app)
    loop.start()
    time.sleep(0.3)

    assert ez_app.state == AppState.STARTED
