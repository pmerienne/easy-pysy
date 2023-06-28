from typing import Optional

from easy_pysy import Service, AppStarted, AppStopping, on, EzApp


class ImAware(Service):
    state: str = ''
    app_started: Optional[AppStarted] = None
    app_stopping: Optional[AppStopping] = None

    @on(AppStarted)
    def on_app_started(self, event: AppStarted):
        print(f"I'm aware that app was started: {event}")
        self.app_started = event

    @on(AppStopping)
    def on_app_stopping(self, event: AppStopping):
        print(f"I'm aware that app is stopping: {event}")
        self.app_stopping = event

    def start(self):
        print('I was started')
        self.state = 'started'

    def stop(self):
        print('I was stopped')
        self.state = 'stopped'


def test_start_and_stop_listener():
    with EzApp(components=[ImAware]) as app:
        aware = app.container.get(ImAware)
        assert aware.state == 'started'
        assert aware.app_started is not None
        assert aware.app_stopping is None

    assert aware.state == 'stopped'
    assert aware.app_stopping is not None


# TODO: stop exceptions should not block others stop
