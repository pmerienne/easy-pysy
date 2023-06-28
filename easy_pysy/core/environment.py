import os
from datetime import datetime, date
from typing import Type, cast, Union, Any

import pendulum
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel
from pydantic.fields import FieldInfo, ModelField

# TODO: dict and list
SupportedTypes = Union[str, int, float, bool, datetime, date]

dotenv_path = os.getenv('DOTENV_PATH') or find_dotenv(usecwd=True)
load_dotenv(dotenv_path)

profile = os.getenv('EZ_PROFILE')
profile_dotenv_path = find_dotenv(filename=f'.env.{profile}', usecwd=True)
load_dotenv(profile_dotenv_path)


class EnvField(FieldInfo):
    pass


class Environment(BaseModel):  # TODO: class not need !! Should be an util ? but we should move container env logic here !
    _profile: str

    def __init__(self, **data):
        super().__init__(**data)
        self._profile = get_environment_variable('EZ_PROFILE')

    @property
    def profile(self):
        return self._profile

    def get_from_field(self, field: ModelField) -> Any:
        key = field.field_info.extra.get('env') or field.name.upper()
        return get_environment_variable(key, field.type_)

    class Config:
        underscore_attrs_are_private = True


def get_environment_variable(key: str, type_: Type[SupportedTypes] = str, default=None, raise_if_not_found=False) -> SupportedTypes:
    raw = os.getenv(key)

    if raw is None and raise_if_not_found:
        raise ConfigNotFoundError(f'Config {key} not found')
    elif raw is None:
        return default

    if type_ == str:
        return raw
    elif type_ == int:
        return int(raw)
    elif type_ == float:
        return float(raw)
    elif type_ == bool:
        return raw.lower() == 'true' or raw == '1'
    elif type_ == datetime:
        return cast(datetime, pendulum.parse(raw))
    elif type_ == date:
        return cast(datetime, pendulum.parse(raw)).date()
    else:
        raise TypeNotSupportedError(f'Type {type_} is not supported for configuration')


class ConfigNotFoundError(Exception):
    pass


class TypeNotSupportedError(Exception):
    pass
