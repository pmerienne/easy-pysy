from contextlib import asynccontextmanager
from typing import TypeVar, Optional

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field, Extra

from easy_pysy.core.bus import EventBus, Event
from easy_pysy.core.component import Component
from easy_pysy.core.container import Container
from easy_pysy.core.context import set_current_app
from easy_pysy.core.environment import Environment
from easy_pysy.core.loop import LoopManager
from easy_pysy.core.plugin import Plugin
from easy_pysy.plugins.api import API
from easy_pysy.plugins.cli import CLI
from easy_pysy.plugins.ui.plugin import UI
from easy_pysy.utils.common import require

T = TypeVar('T', bound=Component)


class EzApp(BaseModel):
    _container: Container
    _environment: Environment

    fast_api: Optional[FastAPI] = None
    api: Optional[API] = None

    cli: Optional[CLI] = None

    ui: Optional[UI] = None

    profile: Optional[str] = None

    plugins: list[type[Plugin]] = Field(default_factory=list)
    components: list[type[Component]] = Field(default_factory=list)
    providers: dict[type[Component], Component] = Field(default_factory=dict)

    def __init__(self, **data):
        super().__init__(**data)

        # Root plugins
        self.plugins = [EventBus, LoopManager] + self.plugins

        # Init fast api first !
        self.fast_api = FastAPI(lifespan=self.fast_api_lifespan)

        if self.ui:
            self.ui.init_plugin(self)

    def start(self):
        set_current_app(self)

        # Load env
        self._environment = Environment(profile=self.profile)
        self._environment.start()
        self.profile = self._environment.profile

        self._container = Container(
            components=self.plugins + self.components,
            providers=self.providers,
            environment=self._environment,
        )

        # "Manual" Start plugins
        if self.api:
            self.api.start(self)

        self._container.start()

        self._container.get(EventBus).emit(AppStarted(app=self))

    def stop(self):
        self._container.get(EventBus).emit(AppStopping(app=self))
        self._container.stop()

    def run(self, command: str):
        require(self.cli is not None, "Can't run a command : No CLI configured")
        set_current_app(self)
        self.cli.run(command)

    @property
    def container(self):
        return self._container

    def get(self, component_type: type[T]) -> T:
        return self._container.get(component_type)

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

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    class Config:
        underscore_attrs_are_private = True
        arbitrary_types_allowed = True
        extra = Extra.forbid


def current_app(request: Request) -> EzApp:
    return request.state.ez_app


class AppStarted(Event):
    app: EzApp


class AppStopping(Event):
    app: EzApp
