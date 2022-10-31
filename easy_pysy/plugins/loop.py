import logging
from dataclasses import dataclass
from typing import Callable, Optional

import easy_pysy as ez
from easy_pysy.utils.common import Interval

logger = logging.getLogger(__name__)


@dataclass
class Loop:
    interval_ms: int
    callback: Callable
    stop_app_on_error: bool
    auto_start: bool
    interval: Optional[Interval] = None

    def start(self):
        self.interval = Interval(self.interval_ms, self.callback, self.on_error)
        self.interval.start()

    def stop(self):
        self.interval.stop()
        self.interval = None

    def on_error(self, exception: BaseException):
        logger.exception(f'Loop execution failed: {exception}')
        if self.stop_app_on_error:
            ez.shutdown()

    @property
    def running(self):
        return self.interval is not None


loops: list[Loop] = []


@ez.on(ez.AppStarting)
def start(event: ez.AppStarting):
    for loop in loops:
        if loop.auto_start:
            logger.debug(f'Starting {loop}')
            loop.start()


@ez.on(ez.AppStopping)
def stop(event: ez.AppStopping):
    for loop in loops:
        if loop.running:
            loop.stop()


def get_loop(callback: Callable) -> Optional[Loop]:
    # TODO: nice to have :
    # ez._(self.loops).find(lambda loop: loop.callback == callback)
    for loop in loops:
        if loop.callback == callback:
            return loop
    return None


def loop(every_ms: int, stop_app_on_error=True, auto_start=True):
    def decorator(func):
        loops.append(Loop(every_ms, func, stop_app_on_error, auto_start))
        return func
    return decorator
