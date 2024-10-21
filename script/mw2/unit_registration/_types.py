from typing import Callable, Iterable

import mw2.context.mod_creation as ctx
from mw2.creators.unit.abc import UnitCreator
from mw2.metadata.unit import UnitMetadata

from .new_src_unit_pair import NewSrcUnitPair

UnitDelegate = Callable[[ctx.ModCreationContext], NewSrcUnitPair]
UnitsPerXp = tuple[int, int, int, int]
Transport = str | None