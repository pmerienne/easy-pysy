from pydantic import Field

from easy_pysy.core.context import current_app
from easy_pysy.core.service import Service
from easy_pysy.plugins.ui.context import AppContext
from easy_pysy.plugins.ui.element import Element
from easy_pysy.plugins.ui.meta import UIMetaInformation
from easy_pysy.plugins.ui.page import Page
from easy_pysy.plugins.ui.reactivity import ReactiveData
from easy_pysy.plugins.ui.state import UIState, RouterState
from easy_pysy.plugins.ui.store import Store


class UIManager(Service):
    elements: list[type[Element]] = Field(default_factory=list)
    pages: dict[str, type[Page]] = Field(default_factory=dict)
    stores: list[type[Store]] = Field(default_factory=list)
    style_sheets: list[str] = Field(default_factory=list)
    scripts: list[str] = Field(default_factory=list)

    def get_meta_information(self):
        stores = [store.get_meta() for store in self.stores]
        elements = [element_class.get_meta() for element_class in self.elements]
        elements += [page_class.get_meta() for page_class in self.pages.values()]
        routes = {path: page_class.get_meta().tag for path, page_class in self.pages.items()}
        return UIMetaInformation(
            routes=routes, elements=elements, stores=stores,
            style_sheets=self.style_sheets, scripts=self.scripts,
        )

    def get_reactive_class(self, name: str):
        for reactive_data in self.reactive_data:
            if reactive_data.__name__ == name:
                return reactive_data
        raise RuntimeError(f'No reactive class found for {name}')

    def create_reactive_data(self, reactive_name: str, ui_state: UIState) -> ReactiveData:
        reactive_class = self.get_reactive_class(reactive_name)
        context = self.create_app_context(ui_state)

        app = current_app()
        reactive_data = app.container.inject(reactive_class, context=context, **ui_state.state)
        # reactive_data = reactive_class(context=context, **ui_state.state)
        return reactive_data

    def create_app_context(self, ui_state: UIState) -> AppContext:
        app_context = AppContext()

        # Create stores
        for store_class in self.stores:
            store_state = ui_state.stores.get(store_class.__name__) or {}
            store = store_class(context=app_context, **store_state)
            app_context.stores[store_class] = store

        return app_context

    @property
    def reactive_data(self) -> list[type[ReactiveData]]:
        return self.elements + list(self.pages.values()) + self.stores

    def fetch_reactive_state(self, reactive_name: str, router_state: RouterState):
        # print(f'fetch_reactive_data {name}: {context}')
        reactive_class = self.get_reactive_class(reactive_name)
        reactive_state = reactive_class.fetch_state(router_state)

        ui_state = UIState(state=reactive_state, stores={}, router=router_state)
        reactive_data = self.create_reactive_data(reactive_name, ui_state)
        return reactive_data

