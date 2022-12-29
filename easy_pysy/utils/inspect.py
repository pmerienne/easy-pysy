import inspect

from typing import Any


def qual_name(obj: Any):
    object_type = type(obj)
    module = object_type.__module__
    if module == 'builtins':
        return object_type.__qualname__
    return module + '.' + object_type.__qualname__


def get_methods(obj: Any):
    return [
        (name, member)
        for (name, member) in inspect.getmembers(obj)
        if inspect.ismethod(member)
    ]
