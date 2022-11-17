from easy_pysy.utils.functional.dictionary import EzDict, K, V
from easy_pysy.utils.functional.sequence import EzList, T
from easy_pysy.utils.functional.function import bind, bind_all

from typing import Iterable


def magic(value: list[T] | dict[K, V]) -> EzList[T] | EzDict[K, V]:  # TODO: iterable/sequence
    if isinstance(value, Iterable):
        return EzList(value)
    elif isinstance(value, dict):
        return EzDict(value)
    else:
        raise NotImplementedError(f'Unsupported magic: {type(value)}')
