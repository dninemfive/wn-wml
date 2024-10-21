from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair

from ..infantry_weapons import M16A2, M249, SATCHEL_CHARGE


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # MOT. RIFLES.
    with ctx.create_infantry_unit("MOT. ENGINEERS", "US", "Engineers_US", [(M16A2, 7), (M249, 1), (SATCHEL_CHARGE, 1)]) as mot_engineers:
        # insert between engineers and engineers (FLASH)
        mot_engineers.modules.ui.UpgradeFromUnit = 'Engineers_US'
        ctx.get_unit('Engineers_Flash_US').modules.ui.UpgradeFromUnit = mot_engineers
        return mot_engineers