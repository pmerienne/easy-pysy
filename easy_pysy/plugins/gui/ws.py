import os
from pathlib import Path
from typing import Any

from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import easy_pysy as ez
from easy_pysy.plugins.gui import store, component, router
from easy_pysy.plugins.gui.component import Component
from easy_pysy.plugins.gui.router import Route
from easy_pysy.plugins.gui.store import StoreConfig


# TODO: broadwast changes (see https://fastapi.tiangolo.com/advanced/websockets/#handling-disconnections-and-multiple-clients)


class RPCResponse(BaseModel):
    result: Any
    changes: list


class GuiAppConfig(BaseModel):
    components: list[Component]
    routes: list[Route]
    stores: list[StoreConfig]


@ez.api.get("/ez-gui/config")
def get_config():
    return GuiAppConfig(
        components=component.get_components(),
        routes=router.get_routes(),
        stores=store.get_all()
    )


@ez.api.post("/ez-gui/stores/{store_name}/{method_name}")
def rpc_endpoint(store_name: str, method_name: str, arguments: list):
    result, changes = store.call_store_method(store_name, method_name, arguments)
    return RPCResponse(result=result, changes=changes)



current_directory = os.path.dirname(os.path.realpath(__file__))
# gui_static_directory = Path(current_directory) / Path('static')
# gui_static_directory = gui_static_directory.absolute()
gui_static_directory = Path('/home/pierre/sources/ez-gui-vuejs/dist/')  # TODO; change this


# TODO: not here ?
@ez.command(name='start-gui')
def start_gui():
    app_static_directory: Path = Path('gui')
    app_static_directory = app_static_directory.absolute()
    ez.info(f'Starting GUI with: {app_static_directory}')
    ez.info(f'Libs in : {gui_static_directory}')
    ez.api.mount("/ez-gui", StaticFiles(directory=gui_static_directory, check_dir=False), name="ez-gui")
    ez.api.mount("/", StaticFiles(directory=app_static_directory, html=True), name="static")
    ez.api.start_api()
