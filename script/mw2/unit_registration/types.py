from typing import Callable, Iterable

import context.mod_creation
from creators.unit.abc import UnitCreator
from metadata.unit import UnitMetadata
from .new_src_unit_pair import NewSrcUnitPair

UnitDelegate = Callable[[context.mod_creation.ModCreationContext], NewSrcUnitPair]
UnitsPerXp = tuple[int, int, int, int]
Transport = str | None