from typing import ClassVar

from easy_pysy.core.component import Singleton


class Service(Singleton):
    lazy: ClassVar[bool] = False
