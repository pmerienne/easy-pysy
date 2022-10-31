from dataclasses import dataclass
from threading import Thread
from typing import Type, Callable


class Event:
    pass


@dataclass
class EventSubscriber:
    callback: Callable[[Event], str]
    event_type: Type[Event]
    asynchronous: bool


subscribers: list[EventSubscriber] = []


def on(*event_types: Type[Event], asynchronous=False):
    # TODO: auto detect async function?
    def decorator(func):
        for event_type in event_types:
            subscriber = EventSubscriber(func, event_type, asynchronous)
            subscribers.append(subscriber)
        return func
    return decorator


def emit(event: Event):
    event_type = type(event)

    # Synchronous event
    for subscriber in _get_subscribers(event_type):
        if not subscriber.asynchronous:
            _notify_subscriber(event, subscriber)
        else:
            _async_notify_subscriber(event, subscriber)


def _get_subscribers(event_type: Type[Event]) -> list[EventSubscriber]:
    return [
        subscriber
        for subscriber in subscribers
        if issubclass(event_type, subscriber.event_type)
    ]


def _notify_subscriber(event: Event, subscriber: EventSubscriber):
    subscriber.callback(event)


def _async_notify_subscriber(event: Event, subscriber: EventSubscriber):
    thread = Thread(target=_notify_subscriber, args=(event, subscriber), daemon=True)
    thread.start()

