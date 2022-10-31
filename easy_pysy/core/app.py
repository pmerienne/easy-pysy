import enum
from dataclasses import dataclass
from typing import TypeVar

from easy_pysy.core import logging
from easy_pysy.core import signal
from easy_pysy.core.cli import run_cli
from easy_pysy.core.event import Event, emit
from easy_pysy.utils.common import require

T = TypeVar('T')


class AppState(enum.Enum):
    STOPPED = 1
    STARTING = 2
    STARTED = 3
    STOPPING = 4


class EzContext:
    state = AppState.STOPPED


context = EzContext()


def start():
    require(context.state == AppState.STOPPED, f"Can't start application, current state: {context.state}]")

    logging.info('Starting')
    context.state = AppState.STARTING
    emit(AppStarting())

    logging.info('Started')
    context.state = AppState.STARTED
    emit(AppStarted())


def stop():
    require(context.state == AppState.STARTED, f"Can't stop application, current state: {context.state}")
    logging.info(f'Stopping')
    context.state = AppState.STOPPING
    emit(AppStopping())

    logging.info('Stopped')
    context.state = AppState.STOPPED


def run(auto_start=True):
    if auto_start and context.state == AppState.STOPPED:
        start()
    run_cli()


@dataclass
class AppStarting(Event):
    pass


@dataclass
class AppStarted(Event):
    pass


@dataclass
class AppStopping(Event):
    pass


def shutdown(exit_code=0):
    stop()
    exit(exit_code)


signal.sigint_callback = shutdown
