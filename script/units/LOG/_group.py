from unit_registration.division_unit_registry import DivisionUnitRegistry
from unit_registration.unit_group import UnitGroup
from utils.types.message import Message

from .cmd_m997_tc3v import create as cmd_m997_tc3v
from .m998_humvee_supply import create as m998_humvee_supply
from unit_registration.unit_registration_info import UnitRegistrationInfo as u

def group(registry: DivisionUnitRegistry, parent_msg: Message | None = None) -> UnitGroup:
    return UnitGroup(
        'LOG',
        registry,
        parent_msg,
        u(cmd_m997_tc3v, 1),
        u(m998_humvee_supply, 2)
    )