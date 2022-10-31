import logging
import threading
import time

from typing import Optional
from uuid import uuid4


logger = logging.getLogger(__name__)


# TODO: create an EzThread
class Interval:
    def __init__(self, interval_ms, callback, on_error_callback, daemon=True, *args, **kwargs):
        self.interval_ms = interval_ms
        self.callback = callback
        self.on_error_callback = on_error_callback
        self.daemon = daemon
        self.args = args
        self.kwargs = kwargs

        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=self.daemon)

    def _run(self):
        next_time = time.time() + self.interval_seconds
        while not self.stop_event.wait(next_time - time.time()):
            try:
                next_time += self.interval_seconds
                self.callback(*self.args, **self.kwargs)
            except BaseException as exc:
                self.on_error_callback(exc)

    def start(self):
        if self.thread.is_alive():
            raise RuntimeError('Interval already started')
        self.thread.start()

    def stop(self):
        if not self.thread.is_alive():
            raise RuntimeError('Thread already stopped')
        self.stop_event.set()

    @property
    def interval_seconds(self) -> float:
        return self.interval_ms / 1000.0


def uuid() -> str:
    return str(uuid4())


def require(condition: bool, message: Optional[str] = None, exception: Optional[BaseException] = None):
    if not condition:
        exception = exception or RequirementError(message)
        raise exception


class RequirementError(Exception):
    pass


class IntSequence:
    _last_id = 0

    def create_new_id(self) -> int:
        self._last_id += 1
        return self._last_id
