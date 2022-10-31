import os
from datetime import datetime, date
from pathlib import Path
from typing import Type, cast

import pendulum
from dotenv import load_dotenv

from easy_pysy.core import logging

# TODO: dict and list
SupportedTypes = str | int | float | bool | datetime | date
dotenv_path = os.getenv('DOTENV_PATH')
dotenv_path = Path(dotenv_path) if dotenv_path else Path(os.getcwd(), '.env').resolve()

logging.info(f'Loading dotenv from {dotenv_path}')
load_dotenv(dotenv_path)


def config(key: str, config_type: Type[SupportedTypes] = str, default=None, raise_if_not_found=False) -> SupportedTypes:
    raw = os.getenv(key)

    if raw is None and raise_if_not_found:
        raise ConfigNotFoundError(f'Config {key} not found')
    elif raw is None:
        return default

    if config_type == str:
        return raw
    elif config_type == int:
        return int(raw)
    elif config_type == float:
        return float(raw)
    elif config_type == bool:
        return raw.lower() == 'true' or raw == '1'
    elif config_type == datetime:
        return cast(datetime, pendulum.parse(raw))
    elif config_type == date:
        return cast(datetime, pendulum.parse(raw)).date()
    else:
        raise TypeNotSupportedError(f'Type {config_type} is not supported for configuration')


class ConfigNotFoundError(Exception):
    pass


class TypeNotSupportedError(Exception):
    pass
