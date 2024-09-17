from typing import Self
from uuid import uuid4

from utils.types.cache import Cache


class GuidManager(object):
    def __init__(self: Self, cache: Cache):
        self._cache = cache
    
    def generate(self: Self, guid_key: str) -> str:
        """ Generates a GUID in the format NDF expects """
        if guid_key in self._cache:
            return self._cache[guid_key]
        result: str = f'GUID:{{{str(uuid4())}}}'
        self._cache[guid_key] = result
        return result