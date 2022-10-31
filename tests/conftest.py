import pytest
from _pytest.fixtures import FixtureRequest

import easy_pysy as ez
from easy_pysy.core.lifecycle import AppState


events = ez.EzList[ez.Event]()


@pytest.fixture
def ez_app(request: FixtureRequest):
    ez.start()
    yield ez.context
    if ez.context.state == AppState.STARTED:
        ez.stop()


@ez.on(ez.Event)
def log_event(event: ez.Event):
    events.append(event)


@ez.on(ez.AppStopping)
def clear_on_stop(event: ez.AppStopping):
    events.clear()
