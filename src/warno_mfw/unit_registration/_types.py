from typing import Any, Callable

import warno_mfw.context.mod_creation as ctx

from .new_src_unit_pair import NewSrcUnitPair

# actual signature is [[ModCreationContext], NewSrcUnitPair], but Python is stupid
UnitDelegate = Callable[[Any], NewSrcUnitPair]
UnitsPerXp = tuple[int, int, int, int]
Transport = str | None