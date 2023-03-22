import pytest
from pydantic import BaseModel, Field

import easy_pysy as ez

from easy_pysy.plugins import repository


class Todo(BaseModel):
    id: str = Field(default_factory=ez.uuid)
    name: str
    done: bool


@pytest.fixture
def todo_list():
    todo_list = repository.get(Todo)
    todo_list.delete_all()
    yield todo_list
    todo_list.delete_all()


def test_repository_should_save(todo_list):
    # Given 2 tasks
    task_1 = Todo(name='Task 1', done=False)
    task_2 = Todo(name='Task 2', done=True)

    # When I save them
    todo_list.save(task_1)
    todo_list.save(task_2)

    # Then I can list them
    tasks = todo_list.find_all()
    assert len(tasks) == 2
    assert task_1 in tasks
    assert task_2 in tasks


def test_repository_should_get_by_id(todo_list):
    # Given a saved tasks
    task_1 = todo_list.save(Todo(name='Task 1', done=False))

    # Then
    assert task_1 == todo_list.get_by_id(task_1.id)
    assert todo_list.get_by_id('bad id') is None

