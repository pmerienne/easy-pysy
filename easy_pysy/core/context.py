from typing import TypeVar, Optional

from easy_pysy.core.component import Component

T = TypeVar('T', bound=Component)

_current_app: Optional['EzApp'] = None


def get(component_type: type[T]) -> T:
    app = current_app()
    return app.container.get(component_type)


def current_app() -> 'EzApp':
    return _current_app


def set_current_app(app: 'EzApp'):
    global _current_app
    _current_app = app


inject = get
