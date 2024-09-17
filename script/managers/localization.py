import random
import string
from typing import Self

from utils.types.cache import Cache
from utils.types.message import Message, try_nest

CHARACTERS = [*string.ascii_letters, *[str(x) for x in range(10)]]

class LocalizationManager(object):
    def __init__(self: Self, cache: Cache, prefix: str):
        if len(prefix) > 5:
            raise Exception("Localization prefix cannot be longer than 5 characters, as keys must be 10 or fewer characters total!")
        self._cache = cache
        self.prefix = prefix
    
    def register(self: Self, string: str) -> str:
        """ Registers a localized string in the localization cache. Returns the __key__ generated for this string! """
        if string in self._cache:
            return f"'{self._cache[string]}'"
        key = self.generate_key()
        while key in self._cache.values:
            key = self.generate_key()
        # intentionally backward: we want to be able to look up strings by their values to get their tokens
        self._cache[string] = key
        return f"'{key}'"

    def generate_key(self: Self) -> str:
        result = self.prefix
        for _ in range(10 - len(result)):
            result += random.choice(CHARACTERS)
        return result

    def generate_csv(self: Self, msg: Message | None) -> str:
        result = '"TOKEN";"REFTEXT"'
        with try_nest(msg, "Generating localization") as msg2:
            for k in sorted(self._cache.keys):
                with msg2.nest(f"{self._cache[k]}\t{k}") as _:
                    result += "\n" + f'"{self._cache[k]}";"{k}"'
        return result