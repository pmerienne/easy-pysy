from contextlib import asynccontextmanager
from typing import TypeVar

from fastapi import FastAPI, APIRouter, Request
from pydantic import BaseModel, Field

from easy_pysy.core_oop.bus import EventBus
from easy_pysy.core_oop.component import Component
from easy_pysy.core_oop.environment import Environment
from easy_pysy.core_oop.ioc import Container
from easy_pysy.core_oop.loop import LoopManager
from easy_pysy.core_oop.plugin import Plugin

T = TypeVar('T', bound=Component)


class EzApp(BaseModel):
    _container: Container
    _environment: Environment

    plugins: list[type[Plugin]] = Field(default_factory=list)
    components: list[type[Component]] = Field(default_factory=list)

    def __init__(self, **data):
        super().__init__(**data)

        # Root plugins
        self.plugins = [EventBus, LoopManager] + self.plugins

    @asynccontextmanager
    async def fast_api_lifespan(self, app: FastAPI):
        self.start()
        yield
        print('LIFESPAN TEARDOWN', self, app)
        # TODO: stop

    def include_ez_app(self, request: Request):
        request.state.ez_app = self

    def start(self):
        self._environment = Environment()
        self._container = Container(
            components=self.plugins + self.components,
            environment=self._environment,
        )

        self._container.start()

    @property
    def container(self):
        return self._container

    def get(self, component_type: type[T]) -> T:
        return self._container.get(component_type)

    class Config:
        underscore_attrs_are_private = True


def current_app(request: Request) -> EzApp:
    return request.state.ez_app
