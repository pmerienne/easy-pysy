from dictdiffer import diff

import easy_pysy as ez
from easy_pysy.plugins.gui.model import GuiStore, GuiStoreConfig

stores: dict[str, GuiStore] = {}


def get_or_create_store(store_id: str) -> GuiStore:
    if store_id not in stores:
        stores[store_id] = GuiStore(id=store_id)
    return stores[store_id]


def get_config() -> list[GuiStoreConfig]:
    return [GuiStoreConfig.from_store(store) for store in stores.values()]


def call_store_method(store_id: str, action_name: str, args: list):
    ez.info(f'Calling {action_name} with {args} on {store_id}')

    ez.require(store_id in stores, f'No store found for {store_id}')
    store = stores[store_id]
    function = store.get_action(action_name)

    original = store.get_jsonable_data()
    result = function(*args)
    modified = store.get_jsonable_data()
    changes = diff(original, modified)

    return result, changes
