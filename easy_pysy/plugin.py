from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from easy_pysy.core import App


class Plugin:
    app: Optional['App'] = None

    def init(self, app):
        self.app = app

    def start(self):
        pass

    def stop(self):
        pass
