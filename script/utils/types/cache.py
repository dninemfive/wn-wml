from utils.io import load, write
from message import Message, try_nest
from typing import Generator, Self

class Cache(object):
    def __init__(self: Self, file_path: str):
        self.file_path = file_path
        self._data: dict[str, str] = None

    def __getitem__(self: Self, key: str) -> str:
        return self._data[key]

    def load(self: Self, parent_msg: Message | None = None) -> None:
        with try_nest(parent_msg, self.file_path) as _:
            self._data = load(self.file_path, {})

    def save(self: Self, parent_msg: Message | None = None) -> None:
        with try_nest(parent_msg, self.file_path) as _:
            write(self._data, self.file_path)

    @property
    def keys(self: Self) -> Generator[str]:
        yield from self._data.keys()

    @property
    def values(self: Self) -> Generator[str]:
        yield from self._data.values()