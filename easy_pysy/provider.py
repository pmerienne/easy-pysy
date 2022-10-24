from dataclasses import dataclass
from typing import TypeVar, Type, Callable, Generic, Any

from easy_pysy.utils import require
from easy_pysy.plugin import Plugin
import easy_pysy as ez

T = TypeVar('T')
ProviderFactory = Callable[[], T]


@dataclass
class Provider(Generic[T]):
    type: Type[T]
    factory: ProviderFactory
    singleton: bool


_all_providers: list[Provider] = []


class ProviderPlugin(Plugin):
    providers: dict[Type, Provider] = {}
    singletons: dict[Type, Any] = {}

    def start(self):
        self.providers = {
            provider.type: provider
            for provider in _all_providers
            if self.app.is_available(provider.factory)
        }


def provide(type: Type[T], singleton: bool = False):
    # TODO: auto detect async function?
    def decorator(func):
        _all_providers.append(Provider(type, func, singleton))
        return func
    return decorator


def get(type: Type[T]) -> T:  # TODO: other name
    plugin = ez.plugin(ProviderPlugin)
    require(type in plugin.providers, f"No provider found for {type}")
    provider = plugin.providers[type]

    # TODO you can write better
    if not provider.singleton:
        return provider.factory()
    elif type not in plugin.singletons:
        instance = provider.factory()
        plugin.singletons[type] = instance
        return instance
    else:
        return plugin.singletons[type]
