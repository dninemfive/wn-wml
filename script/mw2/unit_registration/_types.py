from typing import Callable

import mw2.context.mod_creation as ctx

from .new_src_unit_pair import NewSrcUnitPair

UnitDelegate = Callable[[ctx.ModCreationContext], NewSrcUnitPair]
UnitsPerXp = tuple[int, int, int, int]
Transport = str | None