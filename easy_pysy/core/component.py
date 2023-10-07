from typing import ClassVar

from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo


class Inject(FieldInfo):
    def __init__(self, *args, **kwargs):
        kwargs['exclude'] = True
        super().__init__(*args, **kwargs)


class Injectable(BaseModel):
    class Config:
        keep_untouched = (Inject, )


class Component(Injectable):
    profile: ClassVar[str] = '*'
    lazy: ClassVar[bool] = True

    @classmethod
    def has_profile(cls, profile: str):
        return cls.profile == '*' or cls.profile == profile

    def start(self):
        pass

    def stop(self):
        pass

    class Config:
        arbitrary_types_allowed = True


class Singleton(Component):
    profile: ClassVar[str] = '*'


class PostProcessor(Component):
    def post_init(self, component: Component):
        pass
