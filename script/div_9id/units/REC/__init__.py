from ..transports import (BLACKHAWK,
                          CHINOOK,
                          FAV,
                          M151A2_M2HB,
                          M35,
                          M998_HUMVEE,
                          REC_HUMVEE_AGL,
                          REC_HUMVEE_M2HB)
from mw2.unit_registration.division_unit_registry import DivisionUnitRegistry
from mw2.unit_registration.unit_group import UnitGroup
from mw2.unit_registration.unit_registration_info import \
    UnitRegistrationInfo as u
from mw2.utils.types.message import Message

from fav_agl                import create as fav_agl
from fav_m2hb               import create as fav_m2hb
from folt                   import create as folt
from iew_team               import create as iew_team
from joh58d_kiowa           import create as joh58d_kiowa
from mot_scouts             import create as mot_scouts
from mqm10_aquila           import create as mqm_10_aquila
from operational_support    import create as osd
from scoutat_team           import create as scout_at_team

FAV_TRANSPORTS = [None, CHINOOK]

def group(registry: DivisionUnitRegistry, parent_msg: Message | None = None) -> UnitGroup:
    return UnitGroup(
        'REC',
        registry,
        parent_msg,
        (
            'FAVs',
            [
                u(fav_m2hb,     2, transports=FAV_TRANSPORTS),
                u(fav_agl,      2, transports=FAV_TRANSPORTS),
                # 👓 FAV TOW
            ]
        ),
        (
            'Infantry',
            [
                u(folt,             2,   [0, 8, 6, 4], [FAV, REC_HUMVEE_AGL, BLACKHAWK]),
                u('LRRP_US',        3,      transports=[M998_HUMVEE, M151A2_M2HB]),
                # CEWI?
                # TODO: when NORTHAG releases, change M35 here to CUCV
                # (or MCT?)
                u(osd,              1,   [0, 6, 4, 0], [M35, CHINOOK]),
                u(iew_team,         2,      transports=[REC_HUMVEE_M2HB]),
                u(mot_scouts,       2,      transports=[REC_HUMVEE_M2HB, REC_HUMVEE_AGL, BLACKHAWK]),
                u(scout_at_team,    2,      transports=[REC_HUMVEE_M2HB])
            ]
        ),
        (
            'Helicopters',
            [
                u('OH58C_Scout_US',         2),
                u('OH58D_Combat_Scout_US',  2),
                u(joh58d_kiowa,             1),
                u('EH60A_EW_US',            1)
            ]
        ),
        (
            'Planes',
            [
                u(mqm_10_aquila, 2, [6, 0, 0, 0]),
                # [[👓]] F-14D TOMCAT TARPS
            ]
        )
        # TODO: Misc.
        #   - KLR-250? Transported in Humvees?
        #   - M998 HUMVEE G/VLLD (when NORTHAG releases)
    )