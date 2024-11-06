# Iterator instead of Generator: https://stackoverflow.com/a/63237329
import os
from typing import Generic, Iterator, Self, TypeVar

from warno_mfw.utils.io import load, write
from warno_mfw.utils.types.cache_base import CacheBase
from warno_mfw.utils.types.message import Message, try_nest

V = TypeVar('V')

class Cache(CacheBase[V]):
    def _load_data(self: Self) -> dict[str, V]:
        return load(self.file_path, {})

    def _save_data(self: Self, accessed_items: dict[str, V]) -> None:
        write(accessed_items, self.file_path)