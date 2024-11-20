from dataclasses import dataclass
from typing import Literal, Self
from uuid import uuid4

from warno_mfw.utils.types.cache.file import FileCache
from warno_mfw.hints import NationaliteOrAlias
from warno_mfw.hints._validation import _resolve_Nationalite

@dataclass
class CountryInfo(object):
    nationalite: NationaliteOrAlias

    def __post_init__(self: Self):
        self.nationalite = _resolve_Nationalite(self.nationalite)

class CountryManager(object):
    def __init__(self: Self, cache: FileCache):
        ...

    # TODO: register countries here