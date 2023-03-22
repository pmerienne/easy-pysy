from typing import Optional

from easy_pysy.plugins.gui.store import get_or_create_store


def data(store: str, name: Optional[str] = None):
    store = get_or_create_store(store)

    def decorator(func):
        data_name = name or func.__name__
        store.add_data(data_name, func)
        return func

    return decorator


def action(store: str, name: Optional[str] = None):
    store = get_or_create_store(store)

    def decorator(func):
        data_name = name or func.__name__
        store.add_action(data_name, func)
        return func

    return decorator
