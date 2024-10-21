from unit_registration.division_unit_registry import DivisionUnitRegistry
from unit_registration.unit_group import UnitGroup
from utils.types.message import Message

from unit_registration.unit_registration_info import UnitRegistrationInfo as u

def group(registry: DivisionUnitRegistry, parent_msg: Message | None = None) -> UnitGroup:
    return UnitGroup(
        'ART',
        registry,
        parent_msg,
        (
            'Mortars',
            [
                
            ]
        )
    )