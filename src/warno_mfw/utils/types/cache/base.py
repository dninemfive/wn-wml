from collections import defaultdict
from typing import Generic, Iterator, Self, TypeVar

from warno_mfw.utils.types.message import Message, try_nest

V = TypeVar('V')

class BaseCache(Generic[V]):
    def __init__(self: Self,):
        self._data: dict[str, V] = None

    def __getitem__(self: Self, key: str) -> V:
        return self._data[key]
    
    def __setitem__(self: Self, key: str, val: V):
        self._data[key] = val

    def __contains__(self: Self, key: str) -> bool:
        return key in self._data

    def load(self: Self, parent_msg: Message | None = None) -> None:
        raise NotImplemented

    def save(self: Self, parent_msg: Message | None = None) -> None:
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