from contextlib import asynccontextmanager
from typing import TypeVar

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

from easy_pysy.core.bus import EventBus, Event
from easy_pysy.core.component import Component
from easy_pysy.core.container import Container
from easy_pysy.core.environment import Environment
from easy_pysy.core.loop import LoopManager
from easy_pysy.core.plugin import Plugin

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

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    @asynccontextmanager
    async def fast_api_lifespan(self, app: FastAPI):
        """
        Allow easy integration with FastAPI:
        app = EzApp()
        api = FastAPI(lifespan=app.fast_api_lifespan)

        :param app:
        :return:
        """
        self.start()
        yield
        self.stop()

    def start(self):
        self._environment = Environment()
        self._container = Container(
            components=self.plugins + self.components,
            environment=self._environment,
        )

        self._container.start()

        self._container.get(EventBus).emit(AppStarted(app=self))

    def stop(self):
        self._container.get(EventBus).emit(AppStopping(app=self))
        self._container.stop()

    @property
    def container(self):
        return self._container

    def get(self, component_type: type[T]) -> T:
        return self._container.get(component_type)

    class Config:
        underscore_attrs_are_private = True


def current_app(request: Request) -> EzApp:
    return request.state.ez_app


class AppStarted(Event):
    app: EzApp


class AppStopping(Event):
    app: EzApp
