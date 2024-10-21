from typing import Self

from utils.types.message import Message, try_nest

from .division_unit_registry import DivisionUnitRegistry
from .types import UnitRegistrationInfo

class UnitGroup(object):
    def __init__(self: Self, name: str, registry: DivisionUnitRegistry, msg: Message | None = None, *units: UnitRegistrationInfo):
        self.name = name
        self.registry = registry
        self.msg = msg
        self.units = units

    def register_all(self: Self) -> None:
        with try_nest(self.msg, f'Registering unit group {self.name}') as msg:
            for unit, packs, units_per_xp, transports in self.units:
                self.registry.register(unit, packs, units_per_xp, transports)