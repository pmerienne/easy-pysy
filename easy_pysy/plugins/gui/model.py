from typing import Callable, Any

import easy_pysy as ez

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class GuiStore(BaseModel):
    id: str
    data: dict[str, Callable[[], Any]] = {}
    actions: dict[str, Callable[[], Any]] = {}

    @property
    def action_names(self):
        return [name for name in self.actions.keys()]

    def get_action(self, name):
        ez.require(name in self.actions, f'No action found on store {self.id} with name: {name}')
        return self.actions[name]

    def add_data(self, name: str, function: Callable[[], Any]):
        self.data[name] = function

    def add_action(self, name: str, function: Callable[[], Any]):
        self.actions[name] = function

    def get_jsonable_data(self) -> dict[str, Any]:
        raw = {key: function() for key, function in self.data.items()}
        return jsonable_encoder(raw)


class GuiStoreConfig(BaseModel):
    id: str
    data: dict
    actions: list[str]

    @staticmethod
    def from_store(store: GuiStore) -> 'GuiStoreConfig':
        return GuiStoreConfig(
            id=store.id,
            data=store.get_jsonable_data(),
            actions=store.action_names,
        )


class Component(BaseModel):
    name: str
    url: str


class Route(BaseModel):
    path: str
    url: str


class GuiAppConfig(BaseModel):
    components: list[Component]
    routes: list[Route]
    stores: list[GuiStoreConfig]
