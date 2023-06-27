import pytest

import easy_pysy as ez


def test_transactional():
    @ez.transactional()
    def transactional_fn():
        assert ez.current_session() is not None

    def not_transactional_fn():
        with pytest.raises(Exception):
            ez.current_session()

    transactional_fn()
    not_transactional_fn()


def rollback_on_error():
    def save_user(fail: bool)