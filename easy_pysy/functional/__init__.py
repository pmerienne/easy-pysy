from easy_pysy.functional.dictionary import EzDict, K, V
from easy_pysy.functional.sequence import EzList, T, U


def magic(value: list[T] | dict[K, V]) -> EzList[T] | EzDict[K, V]:  # TODO: iterable/sequence
    match value:
        case list():
            return EzList(value)
        case dict():
            return EzDict(value)
        case _:
            raise NotImplementedError(f'Unsupported magic: {type(value)}')
