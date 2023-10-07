from typing import Optional, Any

from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel

from easy_pysy.core.context import inject
from easy_pysy.plugins.ui.reactivity import execute_listeners, execute_method, execute_watchers, execute_effects, Event, \
    UIStateChanges
from easy_pysy.plugins.ui.service import UIManager
from easy_pysy.plugins.ui.state import UIState, RouterState

ui_api = APIRouter()


class ValueChange(BaseModel):
    name: str
    new: Any
    old: Any


class ExecuteReactiveMethod(BaseModel):
    ui_state: UIState
    parameters: list[Any]


class ExecuteEffect(BaseModel):
    ui_state: UIState
    change: Optional[ValueChange]


class ExecuteListeners(BaseModel):
    ui_state: UIState
    event: Event


@ui_api.get('/_ui')
def get_meta():
    ui = inject(UIManager)
    return ui.get_meta_information()


@ui_api.post('/_ui/reactive/{reactive_name:str}')
def fetch_reactive_state(reactive_name: str, router_state: RouterState):
    ui = inject(UIManager)
    return ui.fetch_reactive_state(reactive_name, router_state)


@ui_api.post('/_ui/reactive/{name:str}/_effect')
def execute_reactive_effect(name: str, body: ExecuteEffect) -> UIStateChanges:
    ui = inject(UIManager)
    reactive_data = ui.create_reactive_data(name, body.ui_state)

    if body.change:
        changes = execute_watchers(reactive_data, body.change.name, body.change.new, body.change.old)
    else:
        changes = execute_effects(reactive_data)

    return changes


@ui_api.post('/_ui/reactive/{name:str}/_event')
def execute_reactive_listeners(name: str, body: ExecuteListeners) -> UIStateChanges:
    ui = inject(UIManager)
    reactive_data = ui.create_reactive_data(name, body.ui_state)
    changes = execute_listeners(reactive_data, body.event)
    return changes


# Warning, this API should be declared after execute_reactive_effect and execute_reactive_listeners
@ui_api.post('/_ui/reactive/{name:str}/{method_name:str}')
def execute_reactive_method(name: str, method_name: str, body: ExecuteReactiveMethod) -> UIStateChanges:
    ui = inject(UIManager)
    reactive_data = ui.create_reactive_data(name, body.ui_state)
    state_changes = execute_method(reactive_data, method_name, body.parameters)
    return state_changes


@ui_api.get('/{page_path:path}')
def index_html(page_path: str):
    print(f'Returning index.html for {page_path}')
    return FileResponse(f'ui/index.html')

