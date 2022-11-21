
from contextvars import ContextVar
from typing import Any
from copy import deepcopy


class Context:
    ''' Thread independent storage
    '''
    __slots__ = ('_storage',)

    def __init__(self) -> None:
        storage = ContextVar(f'mindsdb.context<{id(self)}>')
        object.__setattr__(self, '_storage', storage)

    def set_default(self) -> None:
        self._storage.set({
            'company_id': None,
            'user_class': 0
        })

    def __getattr__(self, name: str) -> Any:
        storage = self._storage.get({})
        return storage[name]

    def __setattr__(self, name: str, value: Any) -> None:
        storage = deepcopy(self._storage.get({}))
        storage[name] = value
        self._storage.set(storage)

    def __delattr__(self, name: str) -> None:
        storage = deepcopy(self._storage.get({}))
        if name not in storage:
            raise AttributeError(name)
        del storage['name']
        self._storage.set(storage)

    def dump(self) -> dict:
        storage = deepcopy(self._storage.get({}))
        return storage

    def load(self, storage: dict) -> None:
        self._storage.set(storage)


context = Context()