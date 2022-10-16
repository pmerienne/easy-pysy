import pytest
from _pytest.fixtures import FixtureRequest

import easy_pysi as ez
from easy_pysi.core import AppState


def create_app(request, *args, **kwargs):
    app = ez.App()
    app.modules = kwargs.get('modules', [request.node.module])

    if 'root_directory' in kwargs:
        app.root_directory = kwargs['root_directory']
    if 'dotenv_path' in kwargs:
        app.dotenv_path = kwargs['dotenv_path']

    return app


@pytest.fixture
def ez_app(request: FixtureRequest):
    marker = request.node.get_closest_marker('ez_app')

    if marker and len(marker.args) == 1 and isinstance(marker.args[0], ez.App):
        app = marker.args[0]
    else:
        args = marker.args if marker else []
        kwargs = marker.kwargs if marker else {}
        app = create_app(request, *args, **kwargs)

        app.start()
        yield app
        if app.state == AppState.STARTED:
            app.stop()


