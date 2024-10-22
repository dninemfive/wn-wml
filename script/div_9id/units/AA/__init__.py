from div_9id.units.transports import BLACKHAWK, M35, M998_HUMVEE, M998_HUMVEE_AGL
from mw2.unit_registration.division_unit_registry import DivisionUnitRegistry
from mw2.unit_registration.unit_group import UnitGroup
from mw2.unit_registration.unit_registration_info import \
    UnitRegistrationInfo as u
from mw2.utils.types.message import Message

from .joh58c             import create as joh58c
from .m167a2_pivads_20mm import create as m167a2
from .m998_avenger       import create as avenger
from .stinger_tdar       import create as stinger_tdar
from .xm85_t_chaparral   import create as t_chap

MANPADS_TRANSPORTS = [M998_HUMVEE_AGL, BLACKHAWK]

def group(registry: DivisionUnitRegistry, parent_msg: Message | None = None) -> UnitGroup:
    return UnitGroup(
        'AA',
        registry,
        parent_msg,
        (
            'MANPADS',
            [
                u('MANPAD_Stinger_C_US',    1, transports=MANPADS_TRANSPORTS),
                u(stinger_tdar,             1, transports=MANPADS_TRANSPORTS)
            ]
        ),
        (
            'VSHORAD',
            [
                u(m167a2, 2, transports=M998_HUMVEE),
                # TODO: EXCALIBUR VWC
            ]
        ),
        (
            'SHORAD',
            [
                u(t_chap,   1,    transports=M35),
                u(avenger,  2),
                # TODO: M998 SETTER? (probably not)
                # u(joh58c,   1)
            ]
        )
    )