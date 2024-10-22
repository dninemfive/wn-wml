from mw2.unit_registration.division_unit_registry import DivisionUnitRegistry
from mw2.unit_registration.unit_group import UnitGroup
from mw2.unit_registration.unit_registration_info import \
    UnitRegistrationInfo as u
from mw2.utils.types.message import Message

from .m966_humvee_tow   import create as m966_tow
from .m998_humvee_glhl  import create as m998_glh
from .xm4_slammer       import create as slammer
from .xm4_slammer_agl   import create as slammer_agl
from .rdf_lt            import create as rdflt

def group(registry: DivisionUnitRegistry, parent_msg: Message | None = None) -> UnitGroup:
    return UnitGroup(
        'TNK',
        registry,
        parent_msg,
        (
            'Tanks',
            [
                u(slammer,      2,  (0, 6, 4, 0)),
                u(slammer_agl,  1,  (0, 5, 3, 0)),
                u(rdflt,        1,  (0, 4, 2, 0))
            ]
        ),
        (
            'Humvee ATGMs',
            [
                u(m966_tow,                 4),
                u('M1025_Humvee_TOW_US',    3),
                u(m998_glh,                 1)
            ]
        )
    )