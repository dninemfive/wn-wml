from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair

from ..infantry_weapons import M16A2


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # M224 60mm
    # weapons:
    # - M16A2 x6
    # - M224 60mm x2
    with ctx.create_infantry_unit("M224 60mm", "US", "Rifles_HMG_US", [(M16A2, 6)]) as m224_60mm:
        m224_60mm.modules.ui.UpgradeFromUnit = 'd9_Mk19_40mm_US'
        return m224_60mm