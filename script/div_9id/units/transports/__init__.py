from typing import Callable, Self
from mw2.unit_registration.division_unit_registry import DivisionUnitRegistry
from mw2.unit_registration.unit_group import UnitGroup
from mw2.unit_registration.unit_registration_info import \
    UnitRegistrationInfo as u
from mw2.utils.types.message import Message
from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair

from .fav                import create as fav_
from .m998_humvee_agl    import create as m998_humvee_agl_
from .m998_humvee_m2hb   import create as m998_humvee_m2hb_

# vanilla transports
BLACKHAWK           = "Descriptor_Unit_UH60A_Black_Hawk_US"
CHINOOK             = "Descriptor_Unit_CH47_Chinook_US"
M998_HUMVEE         = "Descriptor_Unit_M998_Humvee_US"
M1025_HUMVEE_MP     = 'Descriptor_Unit_M1025_Humvee_MP_US'
M1038_HUMVEE        = "Descriptor_Unit_M1038_Humvee_US"
M151A2_M2HB         = 'Descriptor_Unit_M151A2_scout_US'
M35                 = 'Descriptor_Unit_M35_trans_US'
REC_HUMVEE_M2HB     = "Descriptor_Unit_M1025_Humvee_scout_US"
REC_HUMVEE_AGL      = "Descriptor_Unit_M1025_Humvee_AGL_nonPara_US"

class Transports(object):
    singleton: Self = None
    def __init__(self: Self, ctx: ModCreationContext):
        Transports.singleton = self
        self.FAV                = Transports._init(ctx, fav_)
        self.M998_HUMVEE_M2HB   = Transports._init(ctx, m998_humvee_m2hb_)
        self.M998_HUMVEE_AGL    = Transports._init(ctx, m998_humvee_agl_)

    @staticmethod
    def _init(ctx: ModCreationContext, delegate: Callable[[ModCreationContext], NewSrcUnitPair]) -> str:
        return delegate(ctx).new_unit.descriptor.name