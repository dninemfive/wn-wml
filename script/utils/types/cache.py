from typing import Generator, Self
from utils.io import load, write
from utils.types.message import Message, try_nest

class Cache(object):
    def __init__(self: Self, file_path: str):
        self.file_path = file_path
        self._data: dict[str, str] = None

    def __getitem__(self: Self, key: str) -> str:
        return self._data[key]
    
    def __setitem__(self: Self, key: str, val: str):
        self._data[key] = val

    def __contains__(self: Self, key: str) -> bool:
        return key in self._data

    def load(self: Self, parent_msg: Message | None = None) -> None:
        with try_nest(parent_msg, self.file_path) as _:
            self._data = load(self.file_path, {})

    def save(self: Self, parent_msg: Message | None = None) -> None:
        with try_nest(parent_msg, self.file_path) as _:
            write(self._data, self.file_path)

    @property
    def keys(self: Self): # -> Generator[str]:
        yield from self._data.keys()

    @property
    def values(self: Self): # -> Generator[str]:
        yield from self._data.values()

    @property
    def items(self: Self): # -> Generator[tuple[str, str]]:
        yield from self._data.items()

    @property
    def any(self: Self) -> bool:
        return len(self._data.keys()) > 0