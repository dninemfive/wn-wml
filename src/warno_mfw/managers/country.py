from dataclasses import dataclass
from typing import Literal, Self
from uuid import uuid4

from warno_mfw.utils.types.cache.file import FileCache
from warno_mfw.hints import CoalitionOrAlias
from warno_mfw.hints._validation import _resolve_Coalition
from ndf_parse.model import List

from warno_mfw.wrappers.country import CountryWrapper

@dataclass
class CountryInfo(object):
    coalition: CoalitionOrAlias

    def __post_init__(self: Self):
        self.coalition = _resolve_Coalition(self.coalition)

class CountryManager(object):
    def __init__(self: Self, cache: FileCache):
        self.countries: dict[str, CountryWrapper] = {}

    def _load_vanilla(self: Self, ndf: dict[str, List]) -> None:
        pass
    # TODO: register countries here