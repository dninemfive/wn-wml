from dataclasses import dataclass
from typing import Literal, Self
from uuid import uuid4

from warno_mfw.utils.types.cache import Cache
from warno_mfw.constants.enums import Nationalite

@dataclass
class CountryInfo(object):
    nationalite: Literal['NATO', 'PACT']

    def __post_init__(self: Self):
        self.nationalite = Nationalite.ensure_valid(self.nationalite)

class CountryManager(object):
    def __init__(self: Self, cache: Cache):
        ...

    # TODO: register countries here