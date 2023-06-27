import pytest

import easy_pysy as ez
from dataclasses import dataclass, field


@dataclass
class User:
    name: str
    age: int
    id: str = field(default_factory=ez.uuid)


users = ez.Repository(User)


@ez.transactional()
def test_basic_operations(ez_app):
    user = User(name="Pierre", age=36)
    users.save(user)
    reloaded = users.get_by_id(user.id)
    assert reloaded == user


def test_rollback():
    bob = User(name="Bob", age=5)
    bob_id = bob.id

    @ez.transactional()
    def save_with_exception():
        users.save(bob)
        raise RuntimeError('Unexpected !')

    with pytest.raises(RuntimeError):
        save_with_exception()
        assert users.get_by_id(bob_id) is None
