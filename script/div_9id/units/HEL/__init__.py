from mw2.unit_registration.division_unit_registry import DivisionUnitRegistry
from mw2.unit_registration.unit_group import UnitGroup
from mw2.unit_registration.unit_registration_info import \
    UnitRegistrationInfo as u
from mw2.utils.types.message import Message

from .ah64a_apache_sead import create as apache_sead

def group(registry: DivisionUnitRegistry, parent_msg: Message | None = None) -> UnitGroup:
    return UnitGroup(
        'HEL',
        registry,
        parent_msg,
        u('AH64_Apache_US',         2),
        u('AH64_Apache_emp1_US',    2),
        u('AH64_Apache_ATAS_US',    1),
        u(apache_sead,              1)
    )