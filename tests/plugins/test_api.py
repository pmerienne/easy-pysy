from fastapi import HTTPException
from pydantic import BaseModel, Field

import easy_pysy as ez
from easy_pysy import uuid, AppStopping


class Foo(BaseModel):
    id: str = Field(default_factory=uuid)
    bar: str


repository: dict[str, Foo] = {}


@ez.api.get('/foo/{foo_id}')
def get_by_id(foo_id: str) -> Foo:
    ez.require(foo_id in repository, exception=HTTPException(status_code=404, detail="Foo not found"))
    return repository.get(foo_id)


@ez.api.post('/foo')
def save(foo: Foo) -> Foo:
    repository[foo.id] = foo
    return foo


@ez.on(AppStopping)
def clear(event: AppStopping):
    repository.clear()


def test_get_and_post():
    client = ez.api.TestClient()
    response = client.get('/foo/42')
    assert response.status_code == 404

    response = client.post('/foo', json={"bar": "Hello"})
    assert response.status_code == 200
    created = response.json()

    response = client.get(f'/foo/{created["id"]}')
    assert response.status_code == 200
    assert response.json() == {"id": created["id"], "bar": "Hello"}
