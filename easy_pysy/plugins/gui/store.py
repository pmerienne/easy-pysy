import easy_pysy as ez

from dictdiffer import diff
from pydantic import BaseModel


class StoreSynchronizer:
    def __init__(self, store):
        self.store = store
        self.original = store.dict()
        self.changes = None

    def __enter__(self):
        pass

    def __exit__(self, *args):
        modified = self.store.dict()
        self.changes = diff(self.original, modified)


_stores: dict[str, BaseModel] = {}


def add_store(name: str, store: BaseModel):
    _stores[name] = store


def _get_store_method_names(store: BaseModel):
    return [
        name
        for (name, member) in ez.get_methods(store)
        if member.__module__ not in ('pydantic.main', 'pydantic.utils', )
    ]


class StoreConfig(BaseModel):
    name: str
    data: dict
    methods: list[str]


def get_all() -> list[StoreConfig]:
    return [
        StoreConfig(name=name, data=store.dict(), methods=_get_store_method_names(store))
        for name, store in _stores.items()
    ]


def call_store_method(store_name: str, method_name: str, args: list):
    ez.info(f'Calling {method_name} with {args} on {store_name}')

    ez.require(store_name in _stores, f'No store found with name {store_name}')
    ez.require(hasattr(_stores[store_name], method_name), f'No method found on store {store_name} with name: {method_name}')
    store = _stores[store_name]
    func = getattr(_stores[store_name], method_name)

    original = store.dict()
    result = func(*args)
    modified = store.dict()
    changes = diff(original, modified)

    return result, changes
