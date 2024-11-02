from typing import Iterable, Self

from utils.types.message import Message, try_nest

from .division_unit_registry import DivisionUnitRegistry
from .unit_registration_info import UnitRegistrationInfo

UnitSubgroup = Iterable[UnitRegistrationInfo]
NamedUnitSubgroup = tuple[str, UnitSubgroup]

class UnitGroup(object):
    def __init__(self: Self, name: str, registry: DivisionUnitRegistry, msg: Message | None = None, *units: UnitRegistrationInfo | NamedUnitSubgroup):
        self.name = name
        self.registry = registry
        self.msg = msg
        self.units = units

    def register_all(self: Self) -> None:
        with try_nest(self.msg, f'Registering unit group {self.name}') as msg:
            def register_subgroup(name: str | None, units: Iterable[UnitRegistrationInfo]) -> None:
                msg_str = f' {name}' if name is not None else ''
                with msg.nest(f'Registering subgroup{msg_str}') as _:
                    for info in units:
                        self.registry.register(info.unit, info.packs, info.units_per_xp, info.transports)
            for item in self.units:
                if isinstance(item, UnitRegistrationInfo):
                    self.registry.register(item.unit, item.packs, item.units_per_xp, item.transports)
                elif isinstance(item, tuple):
                    name, units = item
                    register_subgroup(name, units)
                elif isinstance(item, Iterable):
                    register_subgroup(None, item)