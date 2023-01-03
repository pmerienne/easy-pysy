import os
from pathlib import Path

from pydantic import BaseModel


class Route(BaseModel):
    path: str
    url: str


pages_directory = Path('gui/pages')
dynamic_routes: list[Route] = []


def get_routes() -> list[Route]:
    pages = get_pages()
    routes = pages + dynamic_routes
    return routes


def get_pages() -> list[Route]:
    return [
        Route(
            path=f'/{path[:-4]}',  # remove .vue extension
            url=f'pages/{path}'

        )
        for path in os.listdir(pages_directory)
        if path.endswith('.vue')
    ]


def add_dynamic_route(path: str, url: str) -> Route:
    route = Route(path=path, url=url)
    dynamic_routes.append(route)
    return route
