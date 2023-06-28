import inspect
from datetime import datetime
from typing import Callable, Tuple

from pydantic import BaseModel, Field

from easy_pysy.core.component import Component
from easy_pysy.core.plugin import Plugin
from easy_pysy.utils.inspect import qual_name


class Event(BaseModel):
    at = datetime.now()

    @property
    def event_type(self):
        return qual_name(self)

    class Config:
        arbitrary_types_allowed = True


def on(*event_types: type[Event], asynchronous=False):
    # TODO: auto detect async function? for asynchronous
    def decorator(func):
        func.__ez_subscriber__ = EventSubscriber(callback=func, event_types=event_types, asynchronous=asynchronous)
        return func
    return decorator


class EventSubscriber(BaseModel):
    callback: Callable[[Event], None]
    event_types: Tuple[type[Event]]
    asynchronous: bool

    @property
    def method_name(self):
        return self.callback.__name__

    def execute(self, component: Component, event: Event):
        method = getattr(component, self.method_name)
        method(event)


class EventBus(Plugin):
    subscribers: dict[type[Event], list[(Component, EventSubscriber)]] = Field(default_factory=dict)

    def emit(self, event: Event):
        component_subscribers = self.subscribers.get(type(event), [])  # TODO: issubclass
        for (component, subscriber) in component_subscribers:
            subscriber.execute(component, event)

    def post_init(self, component: Component):
        for subscriber in get_event_subscribers(component):
            for event_type in subscriber.event_types:
                if event_type not in self.subscribers:
                    self.subscribers[event_type] = []

                self.subscribers[event_type].append((component, subscriber))

    def stop(self):
        self.subscribers.clear()


def get_event_subscribers(component: Component) -> list[EventSubscriber]:
    subscriber_methods = inspect.getmembers(component, predicate=lambda member: hasattr(member, '__ez_subscriber__'))
    return [method.__ez_subscriber__ for name, method in subscriber_methods]


