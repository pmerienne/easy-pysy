import time
from dataclasses import dataclass

import easy_pysy as ez

COUNTERS = {"sync": 0, "async": 0}


class PingEvent(ez.Event):
    message: str


@ez.on(PingEvent)
def pong_increase(event: PingEvent):
    COUNTERS['sync'] = COUNTERS['sync'] + 1


@ez.on(PingEvent, asynchronous=True)
def pong_increase_async(event: PingEvent):
    time.sleep(0.100)
    COUNTERS['async'] = COUNTERS['async'] + 1


def test_ping_pong(ez_app):
    # When an event is emitted
    ez.emit(PingEvent(message='Hello'))

    # Then synchronous subscribers have been notified
    assert COUNTERS['sync'] == 1

    # And asynchronous subscribers too
    time.sleep(0.2)
    assert COUNTERS['async'] == 1

    # And it has been logged
    events = ez.event.find_by_type(PingEvent)
    assert events == [PingEvent(message='Hello')]


# TODO: app lifecycle event