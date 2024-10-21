import context.mod_creation
from typing import Callable
from creators.unit.abc import UnitCreator

UnitDelegate = Callable[[context.mod_creation.ModCreationContext], UnitCreator]
UnitsPerXp = tuple[int, int, int, int]
Transport = str | None