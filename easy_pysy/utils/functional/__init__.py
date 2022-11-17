from easy_pysy.utils.functional.dictionary import EzDict, K, V
from easy_pysy.utils.functional.sequence import EzList, T
from easy_pysy.utils.functional.function import bind, bind_all

from typing import Iterable, Union


def magic(value: Union[list[T], dict[K, V]]) -> Union[EzList[T], EzDict[K, V]]:  # TODO: iterable/sequence
    if isinstance(value, dict):
        return EzDict(value)
    elif isinstance(value, Iterable):
        return EzList(value)
    else:
        raise NotImplementedError(f'Unsupported magic: {type(value)}')
