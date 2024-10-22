from mw2.unit_registration.division_unit_registry import DivisionUnitRegistry
from mw2.unit_registration.unit_group import UnitGroup
from mw2.unit_registration.unit_registration_info import \
    UnitRegistrationInfo as u
from mw2.utils.types.message import Message

def group(registry: DivisionUnitRegistry, parent_msg: Message | None = None) -> UnitGroup:
    return UnitGroup(
        'AIR',
        registry,
        parent_msg,
        # A-6E INTRUDER
        #   [HE]
        #   [CLU]
        #   [LGB]
        #   SWIP
        # EA-6B PROWLER
        #   [SEAD]
        #   [EW]
        # A-7E CORSAIR II
        #   [HE]
        #   [NPLM]
        #   [SEAD]
        # F-14B TOMCAT
        #   [AA1]
        #   [AA2]
        #   [LGB]        
    )