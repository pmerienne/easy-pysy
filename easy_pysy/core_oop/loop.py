import inspect
from functools import partial
from typing import Callable

from pydantic import BaseModel, Field

from easy_pysy import require, Interval
from easy_pysy.core_oop.component import PostProcessor, Component
from easy_pysy.core_oop.plugin import Plugin


def loop(every_ms: int, stop_app_on_error=True, auto_start=True):
    # TODO: auto detect async function? for asynchronous
    def decorator(func):
        func.__ez_loop__ = Loop(method=func, every_ms=every_ms, stop_app_on_error=stop_app_on_error, auto_start=auto_start)
        return func
    return decorator


class Loop(BaseModel):
    method: Callable[[], None]
    every_ms: int
    stop_app_on_error: bool
    auto_start: bool

    @property
    def method_name(self):
        return self.method.__name__

    def execute(self, component: Component):
        method = getattr(component, self.method_name)
        method()

    class Config:
        allow_mutation = False
        frozen = True


class LoopManager(Plugin):
    intervals: dict[Loop, Interval] = Field(default_factory=dict)

    def post_init(self, component: Component):
        for loop in get_loops(component):
            self.start_loop(component, loop)  # TODO: if auto_start

    def start_loop(self, component: Component, loop: Loop):
        require(loop not in self.intervals, "Loop is already running")

        callback = partial(loop.execute, component)
        interval = Interval(loop.every_ms, callback, self.on_error)
        interval.start()

        self.intervals[loop] = interval

        # ez.emit(LoopStarted(loop=self))

    def stop_loop(self, loop: Loop):
        require(loop in self.intervals, "Loop is not running")

        interval = self.intervals.pop(loop)
        interval.cancel()

        # ez.emit(LoopStopped(loop=self))

    def on_error(self, exception: BaseException):
        ez.exception(f'Loop execution failed: {exception}')
        if self.stop_app_on_error:
            ez.shutdown()

    class Config:
        arbitrary_types_allowed = True


def get_loops(component: Component) -> list[Loop]:
    loop_methods = inspect.getmembers(component, predicate=lambda member: hasattr(member, '__ez_loop__'))
    return [method.__ez_loop__ for name, method in loop_methods]