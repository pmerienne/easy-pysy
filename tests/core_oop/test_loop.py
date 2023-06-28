import time

from pydantic import Field

from easy_pysy.core_oop.app import EzApp
from easy_pysy.core_oop.component import Service
from easy_pysy.core_oop.loop import loop


class Ticker(Service):
    ticks: list[float] = Field(default_factory=list)

    @loop(every_ms=200)
    def increase(self):
        self.ticks.append(time.time())
        time.sleep(0.100)  # Really useful to ensure intervals are not shifting


def test_loop_should_call_every_ms():
    app = EzApp(components=[Ticker])
    app.start()

    ticker = app.container.get(Ticker)
    nb_ticks = len(ticker.ticks)

    time.sleep(1.010)
    assert len(ticker.ticks) == nb_ticks + 5

# TODO: def test_stop_start_loop():
# TODO: @loop(every_ms=200, stop_app_on_error=True, auto_start=False)
# TODO: @loop(every_ms=200, stop_app_on_error=False, auto_start=False)
# TODO: test_should_stop_app_on_error
# TODO: test_should_not_stop_app_on_error
# TODO: I don't think it will work with multiple Ticket instances (Loop is a key !)