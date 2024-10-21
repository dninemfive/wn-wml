from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair

from ..infantry_weapons import M16A2, M60E3


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # RANGER GUNNERS
    with ctx.create_infantry_unit("RANGER GUNNERS", "US", "Ranger_US", [(M16A2, 7), (M60E3, 1), (M60E3, 1), (M60E3, 1)]) as ranger_gunners:
        ranger_gunners.modules.ui.UpgradeFromUnit = 'Airborne_HMG_US'
        return ranger_gunners