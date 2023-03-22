from pathlib import Path
from typing import Any

from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import easy_pysy as ez
from easy_pysy.plugins.gui import store, component, router
from easy_pysy.plugins.gui.model import GuiAppConfig

# TODO: broadwast changes (see https://fastapi.tiangolo.com/advanced/websockets/#handling-disconnections-and-multiple-clients)


libs_directory = Path('/home/pierre/sources/ez-gui-vuejs/dist/')  # TODO; change this
gui_static_directory = ez.env('gui_static_directory', default='client')
gui_static_directory = Path(gui_static_directory).absolute()

gui_api_root_path = ez.env('gui_api_root_path', default='ez-gui')


class RPCResponse(BaseModel):
    result: Any
    changes: list


@ez.api.get("/ez-gui/config")
def get_config():
    return GuiAppConfig(
        components=component.get_components(),
        routes=router.get_routes(),
        stores=store.get_config(),
        # TODO: add pages and components paths
    )


@ez.api.post("/ez-gui/stores/{store_name}/{method_name}")
def rpc_endpoint(store_name: str, method_name: str, arguments: list):
    result, changes = store.call_store_method(store_name, method_name, arguments)
    return RPCResponse(result=result, changes=changes)


@ez.command(name='start-gui')
def start():
    ez.info(f'Static directory: {gui_static_directory}')
    ez.info(f'Libs in : {libs_directory}')

    ez.api.mount("/ez-gui-libs", StaticFiles(directory=libs_directory, check_dir=False), name="ez-gui-libs")
    ez.api.mount("/", StaticFiles(directory=gui_static_directory, html=True), name="static")
    ez.api.start_api()
