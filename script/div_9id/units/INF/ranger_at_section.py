from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair

from ..infantry_weapons import M16A2


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # RANGER AT SECTION
    # weapons:
    # - M16A2 x10
    # - M67 90mm
    # - M67 90mm
    # - M67 90mm
    with ctx.create_infantry_unit("RANGER AT SECTION", "US", "Ranger_US", [(M16A2, 10)]) as rangers_m67:
        rangers_m67.modules.ui.UpgradeFromUnit = 'd9_RANGERS_M203_US'
        return rangers_m67