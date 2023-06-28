from typing import TypeVar, Any

from pydantic import BaseModel, Field
from pydantic.utils import lenient_issubclass

from easy_pysy.core_oop.bus import EventBus
from easy_pysy.core_oop.component import Component, Singleton, PostProcessor
from easy_pysy.core_oop.environment import EnvField, Environment
from easy_pysy.core_oop.plugin import Plugin

T = TypeVar('T', bound=Component)
ComponentType = type[T]


class Container(BaseModel):  # TODO: rename (conflict with typing.Container)
    environment: Environment
    components: list[ComponentType]

    singleton_instances: dict[type[Component], Component] = Field(default_factory=dict)
    post_processors: list[PostProcessor] = Field(default_factory=list)

    def start(self):
        for component_type in self.components:
            if not component_type.lazy and component_type.has_profile(self.environment.profile):
                self.get(component_type)  # Will instantiate component

    def get(self, component_type: ComponentType) -> T:
        component_type = self._get_implementation_type(component_type)
        if lenient_issubclass(component_type, Singleton):
            return self._get_or_create_singleton(component_type)
        else:
            return self._instantiate(component_type)

    def _get_implementation_type(self, component_type: ComponentType) -> ComponentType:
        for candidate in self.components:
            if issubclass(candidate, component_type) and candidate.has_profile(self.environment.profile):
                return candidate
        raise RuntimeError(f'No implementation found for: {component_type}')

    def _get_or_create_singleton(self, singleton_type: ComponentType) -> T:
        if singleton_type not in self.singleton_instances:
            self.singleton_instances[singleton_type] = self._instantiate(singleton_type)
        return self.singleton_instances[singleton_type]

    def _instantiate(self, component_type: ComponentType) -> T:
        dependencies = self._get_dependencies(component_type)
        environment_fields = self._get_environment_fields(component_type)

        instance = component_type(**dependencies, **environment_fields)

        for post_processor in self.post_processors:
            post_processor.post_init(instance)

        if isinstance(instance, PostProcessor):
            self.post_processors.append(instance)

        instance.start()
        return instance

    def _get_dependencies(self, component_type: ComponentType) -> dict[str, Component]:
        return {
            field.name: self.get(field.type_)
            for field in component_type.__fields__.values()
            if lenient_issubclass(field.type_, Component)
        }

    def _get_environment_fields(self, component_type: ComponentType) -> dict[str, Any]:
        return {
            field.name: self.environment.get_from_field(field)
            for field in component_type.__fields__.values()
            if isinstance(field.field_info, EnvField)
        }
