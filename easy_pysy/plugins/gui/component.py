import os
from pathlib import Path


def get_all(components_directory: Path):
    return [
        path[:-5]  # remove extension .html
        for path in os.listdir(components_directory)
        if path.endswith('.html')
    ]
