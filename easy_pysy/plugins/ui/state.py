from typing import Optional, Any

from pydantic.fields import Field
from pydantic.main import BaseModel

from easy_pysy.plugins.ui.context import Event

ReactiveState = Optional[dict[str, Any]]
Changes = list[tuple]


class RouterState(BaseModel):
    path: str = ''
    params: dict[str, str] = Field(default_factory=dict)
    route: dict = Field(default_factory=dict)


class UIState(BaseModel):
    router: RouterState
    state: ReactiveState
    stores: dict[str, ReactiveState] = Field(default_factory=dict)


class UIStateChanges(BaseModel):
    path: Optional[str]
    state: Changes = Field(default_factory=Changes)
    stores: dict[str, Changes] = Field(default_factory=dict)
    events: list[Event] = Field(default_factory=list)
    commands: list[str] = Field(default_factory=list)

    def add(self, other: 'UIStateChanges'):
        self.state = other.state if other.state else self.state
        self.state = self.state + other.state
        self.stores = {
            store_name: self.stores.get(store_name, []) + other_store_changes
            for store_name, other_store_changes in other.stores.items()
        }
        self.events += other.events
        self.commands += other.commands

