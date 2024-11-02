from dataclasses import dataclass
from typing import Iterable

from . import _types

# TODO: make packs nullable to allow number of packs to be looked up?
@dataclass
class UnitRegistrationInfo(object):
    unit: str | _types.UnitDelegate
    packs: int
    units_per_xp: _types.UnitsPerXp | None = None
    transports: Iterable[_types.Transport] | None = None