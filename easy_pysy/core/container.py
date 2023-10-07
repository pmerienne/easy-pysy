from typing import TypeVar, Any

from pydantic import BaseModel, Field
from pydantic.utils import lenient_issubclass

from easy_pysy.core.component import Component, Singleton, PostProcessor, Injectable, Inject
from easy_pysy.core.environment import EnvField, Environment

I = TypeVar('I', bound=Injectable)
T = TypeVar('T', bound=Component)
InjectableType = type[I]
ComponentType = type[T]


class Container(BaseModel):  # TODO: rename (conflict with typing.Container)
    environment: Environment
    components: list[ComponentType]
    providers: dict[type[Component], Component] = Field(default_factory=dict)

    instances: list[Component] = Field(default_factory=list)
    singleton_instances: dict[type[Component], Component] = Field(default_factory=dict)

    def start(self):
        for provider_type, provided_instance in self.providers.items():
            self._register(provided_instance)
        for component_type in self.components:
            if not component_type.lazy and component_type.has_profile(self.environment.profile):
                self.get(component_type)  # Will instantiate component

    def stop(self):
        for instance in self.instances:
            instance.stop()

        self.instances.clear()
        self.singleton_instances.clear()

    def get(self, component_type: ComponentType) -> T:
        component_type = self._get_implementation_type(component_type)
        if lenient_issubclass(component_type, Singleton):
            return self._get_or_create_singleton(component_type)
        else:
            return self._instantiate(component_type)

    def _get_implementation_type(self, component_type: ComponentType) -> ComponentType:
        candidates = self.components + list(self.providers.keys())

        for candidate_type in candidates:
            if issubclass(candidate_type, component_type) and candidate_type.has_profile(self.environment.profile):
                return candidate_type
        raise RuntimeError(f'No implementation found for: {component_type}')

    def _get_or_create_singleton(self, singleton_type: ComponentType) -> T:
        if singleton_type not in self.singleton_instances:
            self.singleton_instances[singleton_type] = self._instantiate(singleton_type)
        return self.singleton_instances[singleton_type]

    def _instantiate(self, component_type: ComponentType) -> T:
        instance = self.inject(component_type)
        self._register(instance)
        return instance
    
    def inject(self, injectable_type: InjectableType, **kwargs):
        dependencies = self._get_dependencies(injectable_type)
        environment_fields = self._get_environment_fields(injectable_type)

        instance = injectable_type(**dependencies, **environment_fields, **kwargs)
        return instance

    def _register(self, instance: Component):
        self.instances.append(instance)

        if isinstance(instance, Singleton):
            self.singleton_instances[instance.__class__] = instance

        for post_processor in self.post_processors:
            post_processor.post_init(instance)

        instance.start()

    @property
    def post_processors(self):
        return [instance for instance in self.instances if isinstance(instance, PostProcessor)]

    def _get_dependencies(self, injectable_type: InjectableType) -> dict[str, Component]:
        return {
            field.name: self.get(field.type_)
            for field in injectable_type.__fields__.values()
            # if lenient_issubclass(field.type_, Component)
            if isinstance(field.field_info, Inject)
        }

    def _get_environment_fields(self, injectable_type: InjectableType) -> dict[str, Any]:
        return {
            field.name: self.environment.get_from_field(field)
            for field in injectable_type.__fields__.values()
            if isinstance(field.field_info, EnvField)
        }
