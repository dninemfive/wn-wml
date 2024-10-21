from dataclasses import dataclass
from typing import Iterable

from .types import UnitDelegate, UnitsPerXp, Transport

# TODO: make packs nullable to allow number of packs to be looked up?
@dataclass
class UnitRegistrationInfo(object):
    unit: str | UnitDelegate
    packs: int
    units_per_xp: UnitsPerXp | None = None
    transports: Iterable[Transport] | None = None