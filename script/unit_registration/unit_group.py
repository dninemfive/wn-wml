from typing import Self

from .division_unit_registry import DivisionUnitRegistry
from .types import UnitRegistrationInfo

class UnitGroup(object):
    def __init__(self: Self, name: str, registry: DivisionUnitRegistry, *units: UnitRegistrationInfo):
        self.name = name
        self.registry = registry
        self.units = units

    def register_all(self: Self) -> None:
        for unit, packs, units_per_xp, transports in self.units:
            self.registry.register(unit, packs, units_per_xp, transports)