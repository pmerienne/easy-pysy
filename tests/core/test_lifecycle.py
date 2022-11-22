import easy_pysy as ez


@ez.on(ez.AppStopping)
def fail_when_stopping(event: ez.AppStopping):
    raise RuntimeError('Ouch !')


def test_should_stop_even_when_on_stop_fails(ez_app):
    assert ez_app.state == ez.AppState.STARTED
    ez.stop()
    assert ez_app.state == ez.AppState.STOPPED
