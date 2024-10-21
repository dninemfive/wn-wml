from dataclasses import dataclass
from typing import Literal, Self
from uuid import uuid4

from utils.types.cache import Cache
from constants.primitive_types import Nationalite

@dataclass
class CountryInfo(object):
    nationalite: Literal['NATO', 'PACT']

    def __post_init__(self: Self):
        self.nationalite = Nationalite.ensure_valid(self.nationalite)

class CountryManager(object):
    def __init__(self: Self, cache: Cache):
        self._cache = cache
    
    def generate(self: Self, guid_key: str) -> str:
        """ Generates a GUID in the format NDF expects """
        if guid_key in self._cache:
            return self._cache[guid_key]
        result: str = f'GUID:{{{str(uuid4())}}}'
        self._cache[guid_key] = result
        return result