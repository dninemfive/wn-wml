from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair

from ._weapons import COLT_COMMANDO, M16A2, M203, M249


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # RANGERS (M203)
    # weapons:
    # - Colt Commando x4
    # - M16A2 x3 (squad leader + 2 grenadier)
    # - SAW x2
    # - M203 x2 w/ 36rd each
    with ctx.create_infantry_unit("RANGERS (M203)", "US", "Ranger_US", [(COLT_COMMANDO, 4), (M16A2, 3), (M249, 2), (M203, 2)]) as rangers_m203:
        rangers_m203.modules.ui.UpgradeFromUnit = 'Ranger_Dragon_US'
        return rangers_m203