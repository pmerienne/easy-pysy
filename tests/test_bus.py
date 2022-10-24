import time
from dataclasses import dataclass

from easy_pysy import on, emit, Event

COUNTERS = {"sync": 0, "async": 0}


@dataclass
class PingEvent(Event):
    message: str


@on(PingEvent)
def pong_increase(event: PingEvent):
    COUNTERS['sync'] = COUNTERS['sync'] + 1


@on(PingEvent, asynchronous=True)
def pong_increase_async(event: PingEvent):
    time.sleep(0.100)
    COUNTERS['async'] = COUNTERS['async'] + 1


def test_ping_pong(ez_app):
    # When an event is emitted
    emit(PingEvent('Hello'))

    # Then synchronous subscribers have been notified
    assert COUNTERS['sync'] == 1

    # And asynchronous subscribers too
    time.sleep(0.2)
    assert COUNTERS['async'] == 1


# TODO: app lifecycle event