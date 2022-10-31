import pytest
from _pytest.fixtures import FixtureRequest

import easy_pysy as ez
from easy_pysy.core.app import AppState


@pytest.fixture
def ez_app(request: FixtureRequest):
    ez.start()
    yield ez.context
    if ez.context.state == AppState.STARTED:
        ez.stop()


