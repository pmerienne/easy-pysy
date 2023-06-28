import time
from threading import Timer


class Interval(Timer):
    def __init__(self, interval_ms, function, on_error, args=(), kwargs=None):
        super().__init__(
            interval_ms / 1000.0,
            function,
            args=args,
            kwargs=kwargs or {},
        )
        self.on_error = on_error

    def run(self):
        next_time = time.time() + self.interval
        wait_time = next_time - time.time()
        while not self.finished.wait(wait_time):
            try:
                next_time += self.interval
                self.function(*self.args, **self.kwargs)
                wait_time = next_time - time.time()
            except BaseException as exc:
                self.on_error(exc)
                wait_time = next_time - time.time()

    def stop(self):
        self.cancel()
