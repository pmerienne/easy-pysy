import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi import WebSocket

import easy_pysy as ez

current_directory = os.path.dirname(os.path.realpath(__file__))
# gui_static_directory = Path(current_directory) / Path('static')
# gui_static_directory = gui_static_directory.absolute()
gui_static_directory = Path('/home/pierre/sources/alpinejs-eel/dist/')


# TODO: broadwast changes (see https://fastapi.tiangolo.com/advanced/websockets/#handling-disconnections-and-multiple-clients)

@ez.api.websocket("/ez-gui/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text(f"Hello you, from python")
    # TODO: send store
    while True:
        data = await websocket.receive_json()
        ez.info(f'data: {data}')
        ez.info(f'message: {data["message"]}')
        await websocket.send_text(f"Data was: {data}")


@ez.command(name='start-gui')
def start_gui(app_static_directory: Path = Path('gui')):
    app_static_directory = app_static_directory.absolute()
    ez.info(f'Starting GUI with: {app_static_directory}')
    ez.info(f'Libs in : {gui_static_directory}')
    ez.api.mount("/ez-gui", StaticFiles(directory=gui_static_directory, check_dir=False), name="ez-gui")
    ez.api.mount("/", StaticFiles(directory=app_static_directory, html=True), name="static")
    ez.api.start_api()


