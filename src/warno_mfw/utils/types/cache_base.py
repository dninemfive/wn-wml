# Iterator instead of Generator: https://stackoverflow.com/a/63237329
import os
from typing import Generic, Iterator, Self, TypeVar

from warno_mfw.utils.io import load, write
from warno_mfw.utils.types.message import Message, try_nest

DEFAULT_FOLDER = rf"script\_cache"
V = TypeVar('V')

class CacheBase(Generic[V]):
    def __init__(self: Self, name: str, folder: str = DEFAULT_FOLDER):
        self.file_path = os.path.join(folder, f'{name}.cache')
        self._data: dict[str, V] = None
        self._accessed: dict[str, bool] = None

    def __getitem__(self: Self, key: str) -> V:
        self._accessed[key] = True
        return self._data[key]
    
    def __setitem__(self: Self, key: str, val: V):
        self._accessed[key] = True
        self._data[key] = val

    def __contains__(self: Self, key: str) -> bool:
        self._accessed[key] = True
        return key in self._data

    def load(self: Self, parent_msg: Message | None = None) -> None:
        with try_nest(parent_msg, self.file_path) as _:
            self._data = self._load_data()
            self._accessed = {x:False for x in self._data.keys()}

    def _load_data(self: Self) -> dict[str, V]:
        raise NotImplemented

    def save(self: Self, parent_msg: Message | None = None) -> None:
        with try_nest(parent_msg, self.file_path) as _:
            self._save_data({k: v for k, v in self._data.items() if self._accessed[k]})

    def _save_data(self: Self, accessed_items: dict[str, V]) -> None:
        raise NotImplemented

    @property
    def keys(self: Self) -> Iterator[str]:
        yield from self._data.keys()

    @property
    def values(self: Self) -> Iterator[V]:
        yield from self._data.values()

    @property
    def items(self: Self) -> Iterator[tuple[str, V]]:
        yield from self._data.items()

    @property
    def any(self: Self) -> bool:
        return len(self._data.keys()) > 0