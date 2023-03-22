import json
import os
from pathlib import Path
from typing import get_args, Optional

import easy_pysy as ez
from easy_pysy.plugins.repository.model import Repository, T

root_path = ez.env('ez.file_repository.root_path', default='/tmp')


class FileRepository(Repository[T]):
    def save(self, model: T) -> T:
        models = self._get_all()
        models[model.id] = model
        self._save_all(models)
        return model

    def delete_all(self):
        if self.model_file.exists():
            os.remove(self.model_file)

    def delete(self, model: T):
        self.delete_by_id(model.id)

    def delete_by_id(self, model_id: str):
        models = self._get_all()

        if model_id in models:
            del models[model_id]

        self._save_all(models)

    def get_by_id(self, model_id: str) -> Optional[T]:
        models = self._get_all()
        return models.get(model_id)

    def find_all(self) -> list[T]:
        models = self._get_all()
        return list(models.values())

    @property
    def model_file(self) -> Path:
        return Path(root_path, f'{self.model_type.__name__}.json')

    def _get_all(self) -> dict[str, T]:
        models = {}
        if not self.model_file.exists():
            return models

        with open(self.model_file, 'r') as file:
            for line in file:
                model = self.model_type.parse_raw(line)
                models[model.id] = model

        return models

    def _save_all(self, models: dict[str, T]):
        with open(self.model_file, 'w') as file:
            for model in models.values():
                file.write(model.json())
                file.write('\n')
