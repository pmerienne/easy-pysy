from easy_pysy.plugins.repository.model import Repository, T
from easy_pysy.plugins.repository.file_repository import FileRepository


def get(model_type: type[T]) -> Repository[T]:
    return FileRepository[T](model_type)
