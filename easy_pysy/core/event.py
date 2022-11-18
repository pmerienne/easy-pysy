from dataclasses import dataclass
from threading import Thread
from typing import Type, Callable, TypeVar

from easy_pysy.core.configuration import config
from easy_pysy.core.logging import logger
from easy_pysy.utils.common import require
from easy_pysy.utils.functional.iterable import List
from easy_pysy.utils.inspect import qual_name
from easy_pysy.utils.model import PropertyBaseModel


log_file = config('ez.core.event.log_file')
storage = config('ez.core.event.storage', config_type=bool, default=False)


if log_file:
    logger.add(log_file, format="{message}", filter=__name__, level="DEBUG")


class Event(PropertyBaseModel):
    @property
    def event_type(self):
        return qual_name(self)

    class Config:
        arbitrary_types_allowed = True


@dataclass
class EventSubscriber:
    callback: Callable[[Event], str]
    event_type: Type[Event]
    asynchronous: bool


events = List[Event]()
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

    if log_file:
        logger.info(event.dict())
    if storage:
        events.append(event)

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


EventType = TypeVar('EventType', bound=Type[Event])


def find_by_type(event_type: EventType) -> List[EventType]:
    require(storage, "Storage is not activated. Activate it with env: ez.core.event.storage=True")
    return events.filter(lambda event: isinstance(event, event_type))
