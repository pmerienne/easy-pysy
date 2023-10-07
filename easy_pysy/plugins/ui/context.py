from typing import TypeVar, Optional, Any

from pydantic import BaseModel
from pydantic.fields import Field

T = TypeVar('T')


class Router(BaseModel):
    path: Optional[str] = None

    def navigate(self, path: str):
        self.path = path


class Event(BaseModel):
    type: str
    detail: dict = Field(default_factory=dict)


class Bus(BaseModel):
    events: list[Event] = Field(default_factory=list)

    def dispatch(self, type: str, detail: dict = None):
        event = Event(type=type, detail=detail or {})
        self.events.append(event)


class AppContext(BaseModel):
    router: Router = Router()
    bus: Bus = Bus()
    stores: dict[type['Store'], 'Store'] = Field(default_factory=dict)

    def get_store(self, store_class: type[T]) -> T:
        return self.stores[store_class]
