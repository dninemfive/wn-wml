from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair

from ..infantry_weapons import DRAGON, M16A2, M249


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # MOT. RIFLES (DRAGON)
    with ctx.create_infantry_unit("MOT. RIFLES (DRAGON)", "US", "Rifles_half_Dragon_US", [(M16A2, 6), (M249, 2), (DRAGON, 1)]) as mot_rifles_dragon:        
        mot_rifles_dragon.modules.ui.UpgradeFromUnit='d9_MOT_RIFLES_US'
        mot_rifles_dragon.modules.production.command_point_cost = 65
        return mot_rifles_dragon