from typing import Callable
from typing import TypeVar, Generic

K = TypeVar('K')
V = TypeVar('V')
T = TypeVar('T')
U = TypeVar('U')


class EzList(Generic[T], list[T]):
    def map(self, func: Callable[[T], U]) -> "EzList[U]":
        return EzList([func(v) for v in self])

    def filter(self, predicate: Callable[[T], bool]) -> "EzList[T]":
        return EzList([v for v in self if predicate(v)])
