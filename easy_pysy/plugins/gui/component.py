import os
from pathlib import Path

from easy_pysy.plugins.gui.model import Component

components_directory = Path('client/components')


def get_components() -> list[Component]:
    return [
        Component(
            name=path[:-4],  # remove extension .vue
            url=f'components/{path}'

        )
        for path in os.listdir(components_directory)
        if path.endswith('.vue')
    ]
