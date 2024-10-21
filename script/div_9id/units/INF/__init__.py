from div_9id.units.transports import BLACKHAWK, M1025_HUMVEE_MP, M1038_HUMVEE, M998_HUMVEE, M998_HUMVEE_AGL, M998_HUMVEE_M2HB
from mw2.unit_registration.division_unit_registry import DivisionUnitRegistry
from mw2.unit_registration.unit_group import UnitGroup
from mw2.unit_registration.unit_registration_info import \
    UnitRegistrationInfo as u
from mw2.utils.types.message import Message
from cmd_mot_rifles_ldr import create as mot_rifles_ldr
from m224_60mm import create as m224
from mk19_40mm import create as mk19
from mot_engineers import create as mot_engineers
from mot_mp_patrol import create as mot_mp
from mot_rifles_dragon import create as mot_rifles_dragon
from mot_rifles import create as mot_rifles
from ranger_at_section import create as rangers_at
from ranger_gunners import create as rangers_mg
from rangers_m203 import create as rangers_m203
from m998_humvee_m2hb    import create as m998_m2hb
from m998_humvee_agl    import create as m998_agl

def group(registry: DivisionUnitRegistry, parent_msg: Message | None = None) -> UnitGroup:
    M998_HUMVEE_M2HB = m998_m2hb(registry.ctx).new_unit.descriptor.name
    M998_HUMVEE_AGL  =  m998_agl(registry.ctx).new_unit.descriptor.name
    return UnitGroup(
        'INF',
        registry,
        parent_msg,
        (
            'Mot. Rifles',
            [
                u(mot_rifles_ldr,           2, transports=[M1038_HUMVEE, M998_HUMVEE_M2HB, M998_HUMVEE_AGL, BLACKHAWK]),
                u(mot_rifles,               1, transports=[M1038_HUMVEE,                   M998_HUMVEE_AGL, BLACKHAWK]),
                u(mot_rifles_dragon,        3, transports=[M1038_HUMVEE, M998_HUMVEE_M2HB,                  BLACKHAWK])
            ]
        ),
        (
            'Engineers',
            [
                u('Engineer_CMD_US',        1, transports=[M1038_HUMVEE,                   M998_HUMVEE_AGL]),
                u(mot_engineers,            2, transports=[M1038_HUMVEE,                   M998_HUMVEE_AGL])
            ]
        ),
        (
            'Airborne',
            [
                u('Airborne_CMD_US',        1, transports=[M1038_HUMVEE]),
                u('Airborne_Dragon_US',     1, transports=[M1038_HUMVEE])
            ]
        ),
        (
            'Rangers',
            [
                u(rangers_m203,             1, transports=[M1038_HUMVEE,                   M998_HUMVEE_AGL, BLACKHAWK]),
                u(rangers_at,               1, transports=[M1038_HUMVEE, M998_HUMVEE_M2HB,                  BLACKHAWK]),
                u(rangers_mg,               1, transports=[M1038_HUMVEE, M998_HUMVEE_M2HB,                  BLACKHAWK])
            ]
        ),
        (
            'Support',
            [
                u(mk19,                     1, transports=[M998_HUMVEE,                    M998_HUMVEE_AGL]),
                u(m224,                     1, transports=[M998_HUMVEE,                                     BLACKHAWK])
            ]
        ),
        (
            'Misc',
            [
                u(mot_mp,                   2, transports=[M998_HUMVEE,  M1025_HUMVEE_MP]),
                u('Rifles_Cavalry_US',      2, transports=[              M998_HUMVEE_M2HB, M998_HUMVEE_AGL, BLACKHAWK]),
                u('Rifles_HMG_US',          1, transports=[M1038_HUMVEE, M998_HUMVEE_M2HB,                  BLACKHAWK]),
                u('ATteam_TOW2_US',         3, transports=[M998_HUMVEE,                    M998_HUMVEE_AGL])
            ]
        )
    )