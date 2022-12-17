from typing import Type

from dictdiffer import diff
from pydantic import BaseModel


class GUIStore(BaseModel):
    def sync(self):
        return AlpineStoreSynchronizer(self)

    def transactional(self, fn):
        def decorated(*args, **kwargs):
            with self.sync():
                # TODO: try/catch + revert
                result = fn(*args, **kwargs)
            return result
        # Avoid method not found in alpine
        decorated.__name__ = fn.__name__
        return decorated


class AlpineStoreSynchronizer:
    def __init__(self, store: AlpineStore):
        self.store = store
        self.original = store.dict()

    def __enter__(self):
        pass

    def __exit__(self, *args):
        modified = self.store.dict()
        changes = diff(self.original, modified)
        self.notify_client(list(changes))

    def notify_client(self, changes):
        print(f'Sending changes: {changes}')
        if hasattr(eel, 'updateAlpineStore'):
            eel.updateAlpineStore(changes)
        else:
            print('WARNIONGNGNNGGN no eel.updateAlpineStore')


def init(store_class: Type[AlpineStore]):
    store = store_class()

    @eel.expose
    def get_store():
        return {
            "schema": store.schema(),
            "data": store.dict()
        }
    return store



