from typing import Generator, Self

from utils.types.cache import Cache


class UnitIdManager(object):
    def __init__(self: Self, cache: Cache, initial_id: int):
        self._cache = cache
        self.current_id = initial_id

    @property
    def items(self: Self): # -> Generator[tuple[str, str]]:
        yield from sorted(self._cache.items, key=lambda x: x[1])

    def register(self: Self, descriptor_path: str) -> int:
        if descriptor_path not in self._cache:            
            self._cache[descriptor_path] = str(self.current_id)
            self.current_id += 1
        return self._cache[descriptor_path]