import os
from pathlib import Path

from pydantic import Field
from starlette.staticfiles import StaticFiles

from easy_pysy.core.plugin import Plugin
from easy_pysy.plugins.ui.api import ui_api
from easy_pysy.plugins.ui.element import Element
from easy_pysy.plugins.ui.page import Page
from easy_pysy.plugins.ui.service import UIManager
from easy_pysy.plugins.ui.store import Store
from easy_pysy.utils.common import require


class UI(Plugin):
    elements: list[type[Element]] = Field(default_factory=list)
    pages: dict[str, type[Page]] = Field(default_factory=dict)
    stores: list[type[Store]] = Field(default_factory=list)
    style_sheets: list[str] = Field(default_factory=list)
    scripts: list[str] = Field(default_factory=list)

    def init_plugin(self, app):
        require(app.api is not None, 'UI need api plugin to be activated')
        app.api.apis.append(ui_api)

        # TODO: remove static, its only used to host js lib
        static_dir = Path(os.path.dirname(__file__), "static")
        print('STATIC DIR', Path(static_dir).absolute(), Path(static_dir).exists())

        app.fast_api.mount("/ui/static", StaticFiles(directory=static_dir, follow_symlink=True), name="static")
        app.fast_api.mount("/ui/assets", StaticFiles(directory="ui/assets"), name="assets")

        app.providers[UIManager] = UIManager(
            elements=self.elements, pages=self.pages, stores=self.stores,
            style_sheets=self.style_sheets,
            scripts=self.scripts,
        )
