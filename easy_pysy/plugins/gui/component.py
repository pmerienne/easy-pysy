import os
from pathlib import Path

from pydantic import BaseModel

components_directory = Path('gui/components')


class Component(BaseModel):
    name: str
    url: str


def get_components() -> list[Component]:
    return [
        Component(
            name=path[:-4],  # remove extension .vue
            url=f'components/{path}'

        )
        for path in os.listdir(components_directory)
        if path.endswith('.vue')
    ]
