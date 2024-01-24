import time
from threading import Thread, Event, Timer
from typing import Callable, Optional

from easy_pysy.utils.common import require
from easy_pysy.core.environment import env
from easy_pysy.core.logging import logger
from easy_pysy.core.lifecycle import AppStopping
from easy_pysy.core.event import on

stop_timeout = env('ez.thread.stop_timeout', config_type=int, default=1)


class EzThread(Thread):  # TODO: test
    def __init__(self, target, args=(), kwargs=None, name=None, daemon=False):
        if kwargs is None:
            kwargs = {}
        self.stop_event = Event()
        super().__init__(None, target, name, args, kwargs, daemon=daemon)
        self.target = target

    def start(self):
        require(not self.is_alive(), 'Interval already started')
        self.stop_event.clear()
        threads.append(self)
        super().start()

    def stop(self, timeout=10):
        require(self.is_alive(), 'Thread already stopped')
        self.stop_event.set()
        self.join(timeout)

    def join(self, timeout=None):
        super().join(timeout)
        if self.is_alive():
            assert timeout is not None
            # timeout can't be None here because if it was, then join()
            # wouldn't return until the thread was dead
            raise ZombieThread(f"Thread failed to die within {timeout} seconds")
        else:
            threads.remove(self)


class Interval:
    def __init__(self, interval_ms: float, function: Callable, on_error: Callable, *args, **kwargs):
        self.interval_ms = interval_ms
        self.function = function
        self.on_error = on_error
        self.args = args
        self.kwargs = kwargs
        self.timer: Optional[Timer] = None
        self.start()

    def _run(self):
        self._schedule_next_run()
        try:
            self.function(*self.args, **self.kwargs)
        except Exception as exc:
            self.on_error(exc)

    def start(self):
        if not self.running:
            self._schedule_next_run()

    def _schedule_next_run(self):
        self.timer = Timer(self.interval_ms / 1000.0, self._run)
        self.timer.start()

    def stop(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    @property
    def running(self):
        return self.timer is not None


class ZombieThread(Exception):
    pass


threads: list[EzThread] = []


def get_thread(target: Callable) -> Optional[EzThread]:
    for t in threads:
        if t.target == target:
            return t
    return None


@on(AppStopping)
def on_stop(event: AppStopping):
    logger.debug('Stopping threads')
    while threads:
        running_threads = [thread for thread in threads if thread.is_alive()]
        # Optimization: instead of calling stop() which implicitly calls
        # join(), set all the stopping events simultaneously, *then* join
        # threads with a reasonable timeout
        for thread in running_threads:
            thread.stop_event.set()
        for thread in running_threads:
            logger.debug(f'Stopping thread: {thread}')
            thread.join(stop_timeout)
    logger.debug('Threads stopped')
