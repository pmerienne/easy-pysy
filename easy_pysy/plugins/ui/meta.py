from typing import Any

from pydantic.main import BaseModel


class ReactiveDataMetaInformation(BaseModel):
    name: str
    reactive_values: list[str]
    computed_values: list[str]
    remote_actions: list[str]
    transpiled_actions: dict[str, str]  # name => js code
    watchers: dict[str, list[str]]  # value => function names
    has_effect: bool
    listened_events: list[str]
    data_schema: dict[str, Any]


class ElementMetaInformation(ReactiveDataMetaInformation):
    tag: str
    template: str
    shadow_mode: str


class UIMetaInformation(BaseModel):
    routes: dict[str, str]
    elements: list[ElementMetaInformation]
    stores: list[ReactiveDataMetaInformation]
    style_sheets: list[str]
    scripts: list[str]
