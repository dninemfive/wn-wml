from typing import Callable, Iterable

import context.mod_creation
from creators.unit.abc import UnitCreator
from metadata.unit import UnitMetadata

UnitDelegate = Callable[[context.mod_creation.ModCreationContext], UnitCreator]
UnitsPerXp = tuple[int, int, int, int]
Transport = str | None
UnitRegistrationInfo = tuple[str | UnitDelegate, int, UnitsPerXp | None, Iterable[Transport] | None]