import signal
from typing import Callable, Optional

from easy_pysy.core import logging

exiting = False
sigint_callback: Optional[Callable[[int], None]] = None


def _sigint_handler(signum, frame):
    logging.info(f'Received sigint: {signum}')

    global exiting
    if exiting:
        logging.warning('Double sigint received, forcing exit')
        exit(1)

    exiting = True
    if sigint_callback is not None:
        sigint_callback(signum)


signal.signal(signal.SIGINT, _sigint_handler)
