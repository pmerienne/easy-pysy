import inspect
import threading
from threading import Lock
from typing import Callable, Any, Sequence, Optional

import jsonref
from dictdiffer import diff
from pscript import py2js
from pydantic import BaseModel
from pydantic.fields import Field

from easy_pysy.utils.common import require
from easy_pysy.core.component import Injectable
from easy_pysy.plugins.ui.context import AppContext
from easy_pysy.plugins.ui.meta import ReactiveDataMetaInformation
from easy_pysy.plugins.ui.state import RouterState, UIStateChanges
from easy_pysy.utils import logging


class JSMethod(Callable):
    def __init__(self, js: str):
        self.js = f"function(){{{js}}}"
        self.name: Optional[str] = None

    def __call__(self, *args, **kwargs):
        require(self.name is not None, "Method name is missing")
        current_context.commands.append(self.name)


def js(fn: Callable):  # TODO: remove
    return JSMethod(fn)


class TranspiledFunction:
    def __init__(self, fn):
        self.fn = fn
        self.js = py2js(fn)

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


class WatcherFunction:
    def __init__(self, fn, values: Sequence[str]):
        self.fn = fn
        self.values = values

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


class EffectFunction:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


class EventListenerFunction:
    def __init__(self, fn, event_types: Sequence[str]):
        self.fn = fn
        self.event_types = event_types

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


class Event(BaseModel):
    type: str
    detail: dict


class ComputedFunction:
    def __init__(self, fn):
        self.fn = fn
        self.name = self.fn.__name__

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


def transpiled(fn: Callable):
    return TranspiledFunction(fn)


def computed(fn: Callable):  # TODO: transpiled
    return ComputedFunction(fn)


def effect(fn: Callable):  # TODO: transpiled
    return EffectFunction(fn)


def watch(*values):  # TODO: transpiled
    def decorator(func):
        return WatcherFunction(func, values)
    return decorator


def listener(*event_types):
    def decorator(func):
        return EventListenerFunction(func, event_types)
    return decorator


def worker_with(lock):
    with lock:
        logging.debug('Lock acquired via with')

def worker_not_with(lock):
    lock.acquire()
    try:
        logging.debug('Lock acquired directly')
    finally:
        lock.release()


_context_lock = threading.Lock()
current_context: Optional["ReactiveContext"] = None


class ReactiveContext(object):

    def __init__(self):
        self.commands: list[str] = []

    def __enter__(self):
        global current_context
        current_context = self
        _context_lock.acquire()
        return self

    def __exit__(self, type, value, traceback):
        global current_context
        current_context = None
        _context_lock.release()


class ReactiveData(BaseModel):
    _app_context: AppContext = Field(exclude=True)

    class Config:
        underscore_attrs_are_private = True
        keep_untouched = (
            Injectable,
            AppContext,
            TranspiledFunction, ComputedFunction, JSMethod,
            WatcherFunction, EffectFunction,
            EventListenerFunction,
        )

    def __init__(self, **data):
        context = data.pop('context')  # TODO require context
        super().__init__(**data)
        self._app_context = context
        self._init_js_methods() # TODO: I don't like that

    def _init_js_methods(self):
        for method_name, method in self.get_js_methods().items():
            method.name = method_name

    @property
    def context(self):
        return self._app_context

    @classmethod
    def fetch_state(cls, router_state: RouterState) -> dict[str, Any]:
        return {}

    @classmethod
    def get_meta(cls) -> ReactiveDataMetaInformation:
        return ReactiveDataMetaInformation(
            name=cls.__name__,
            reactive_values=cls.get_reactive_values(),
            computed_values=list(cls.get_computed_values().keys()),
            remote_actions=cls.get_remote_methods(),
            transpiled_actions={**cls.get_transpiled_methods(), ** cls.get_js_methods_code()},
            watchers=cls.get_watchers(),
            has_effect=cls.has_effect(),
            listened_events=cls.get_listened_events(),
            data_schema=jsonref.loads(cls.schema_json()),  # Avoid refs: https://github.com/pydantic/pydantic/issues/889
        )

    @classmethod
    def get_remote_methods(cls):
        base_methods = [name for name, member in inspect.getmembers(ReactiveData) if inspect.isfunction(member)]
        transpiled_methods = cls.get_transpiled_methods().keys()

        methods = [
            name
            for name, member in inspect.getmembers(cls)
            if inspect.isfunction(member)
               and not name.startswith('_')
               and name not in base_methods
               and name not in transpiled_methods
        ]

        return methods

    @classmethod
    def get_transpiled_methods(cls):
        transpiled_methods = {
            name: member.js
            for name, member in inspect.getmembers(cls)
            if isinstance(member, TranspiledFunction)
        }
        return transpiled_methods

    @classmethod
    def get_js_methods(cls) -> dict[str, JSMethod]:
        js_methods = {
            name: member
            for name, member in inspect.getmembers(cls)
            if isinstance(member, JSMethod)
        }
        return js_methods

    @classmethod
    def get_js_methods_code(cls) -> dict[str, JSMethod]:
        js_methods = {
            name: member.js
            for name, member in inspect.getmembers(cls)
            if isinstance(member, JSMethod)
        }
        return js_methods

    @classmethod
    def get_reactive_values(cls):
        field_names = list(cls.__fields__.keys())
        property_names = list(cls.get_computed_values().keys())
        reserved = ['context']
        return [name for name in field_names + property_names if name not in reserved]

    @classmethod
    def get_watchers(cls) -> dict[str, list[str]]:
        watchers = {}
        for name, member in inspect.getmembers(cls):
            if isinstance(member, WatcherFunction):
                for value in member.values:
                    value_watchers = watchers.get(value, [])
                    value_watchers.append(member.fn.__name__)
                    watchers[value] = value_watchers
        return watchers

    @classmethod
    def get_watchers_for(cls, name) -> list[str]:
        return cls.get_watchers()[name]

    @classmethod
    def get_effects(cls) -> list[str]:
        return [
            member.fn.__name__
            for name, member in inspect.getmembers(cls)
            if isinstance(member, EffectFunction)
        ]

    @classmethod
    def has_effect(cls) -> bool:
        return bool(cls.get_effects()) or bool(cls.get_computed_values())

    @classmethod
    def get_computed_values(cls) -> dict[str, ComputedFunction]:
        return {
            name: member
            for name, member in inspect.getmembers(cls)
            if isinstance(member, ComputedFunction)
        }

    @classmethod
    def get_event_listeners(cls) -> dict[str, list[EventListenerFunction]]:
        event_listeners = {}

        for name, member in inspect.getmembers(cls):
            if isinstance(member, EventListenerFunction):
                for event_type in member.event_types:
                    event_type_listeners = event_listeners.get(event_type, [])
                    event_type_listeners.append(member)
                    event_listeners[event_type] = event_type_listeners

        return event_listeners

    @classmethod
    def get_event_listeners_for(cls, event_type: str) -> list[EventListenerFunction]:
        listeners = cls.get_event_listeners()
        return listeners[event_type]

    @classmethod
    def get_listened_events(cls) -> list[str]:
        return list(cls.get_event_listeners().keys())

    def dict(self, *args, **kwargs):
        model_dict = super().dict(*args, **kwargs)

        # Include @computed values
        for name, computed_fn in self.get_computed_values().items():
            model_dict[name] = computed_fn(self)

        return model_dict


def execute_method(reactive_data: ReactiveData, method_name: str, args: list) -> UIStateChanges:
    # 'Save' the original state
    original_state = reactive_data.dict()
    original_store_states = {store_class: store.dict() for store_class, store in reactive_data.context.stores.items()}

    # Call method
    with ReactiveContext() as context:
        method = getattr(reactive_data, method_name)
        result = method(*args)  # TODO: result not used ?

        # Compute state changes
        modified_state = reactive_data.dict()
        state_changes = list(diff(original_state, modified_state))

        # Compute stores' changes
        stores_changes = {}
        for store_class, original_store_state in original_store_states.items():
            modified_store_state = reactive_data.context.stores[store_class].dict()
            store_changes = list(diff(original_store_state, modified_store_state))
            stores_changes[store_class.__name__] = store_changes

        return UIStateChanges(
            path=reactive_data.context.router.path,
            state=state_changes,
            stores=stores_changes,
            events=reactive_data.context.bus.events,
            commands=context.commands
        )


def execute_watchers(reactive_data: ReactiveData, value_name: str, new: Any, old: Any) -> UIStateChanges:
    watchers = reactive_data.get_watchers_for(value_name)
    args = [reactive_data, new, old]

    all_changes = UIStateChanges()
    for method_name in watchers:
        watcher_changes = execute_method(reactive_data, method_name, args)
        all_changes.add(watcher_changes)

    return all_changes


def execute_effects(reactive_data: ReactiveData) -> UIStateChanges:
    all_changes = UIStateChanges()

    # Apply effects
    args = [reactive_data, ]
    for method_name in reactive_data.get_effects():
        effect_changes = execute_method(reactive_data, method_name, args)
        all_changes.add(effect_changes)

    # Always include computed values
    for value_name, computed_value in reactive_data.get_computed_values().items():
        change = ('change', value_name, (None, computed_value(reactive_data)))
        all_changes.state.append(change)

    return all_changes


def execute_listeners(reactive_data: ReactiveData, event: Event) -> UIStateChanges:
    all_changes = UIStateChanges()

    # Call listeners
    for event_listener in reactive_data.get_event_listeners_for(event.type):
        method_name = event_listener.fn.__name__
        args = [reactive_data, event]

        effect_changes = execute_method(reactive_data, method_name, args)
        all_changes.add(effect_changes)

    return all_changes
