from typing import Generic, TypeVar, Optional

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class Repository(Generic[T]):
    def __init__(self, model_type: type[T]):
        self.model_type = model_type

    def save(self, model: T) -> T:
        raise NotImplemented()

    def delete_all(self):
        raise NotImplemented()

    def delete(self, model: T):
        raise NotImplemented()

    def delete_by_id(self, model_id: str):
        raise NotImplemented()

    def get_by_id(self, model_id: str) -> Optional[T]:
        raise NotImplemented()

    def find_all(self) -> list[T]:
        raise NotImplemented()
