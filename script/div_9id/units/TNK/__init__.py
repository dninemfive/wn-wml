from mw2.unit_registration.division_unit_registry import DivisionUnitRegistry
from mw2.unit_registration.unit_group import UnitGroup
from mw2.unit_registration.unit_registration_info import \
    UnitRegistrationInfo as u
from mw2.utils.types.message import Message

from m966_humvee_tow    import create as m966_tow
from m998_humvee_glhl   import create as m998_glh

def group(registry: DivisionUnitRegistry, parent_msg: Message | None = None) -> UnitGroup:
    return UnitGroup(
        'TNK',
        registry,
        parent_msg,
        # TODO: Tanks
        #   XM4 SLAMMER
        #   XM4 SLAMMER AGL
        #   RDF/LT
        (
            'Humvee ATGMs',
            [
                u(m966_tow,                 4),
                u('M1025_Humvee_TOW_US',    3),
                u(m998_glh,                 1)
            ]
        ),
        # TODO: Humvee Fire Support (i.e. M1025 Humvee AGL) (maybe put in INF instead?)
    )