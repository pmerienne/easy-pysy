from typing import ClassVar

from pydantic import BaseModel


class Component(BaseModel):
    profile: ClassVar[str] = '*'
    lazy: ClassVar[bool] = True

    @classmethod
    def has_profile(cls, profile: str):
        return cls.profile == '*' or cls.profile == profile

    def start(self):
        pass

    def stop(self):
        pass


class Singleton(Component):
    profile: ClassVar[str] = '*'


class Service(Singleton):
    lazy: ClassVar[bool] = False


class PostProcessor(Component):
    def post_init(self, component: Component):
        pass
