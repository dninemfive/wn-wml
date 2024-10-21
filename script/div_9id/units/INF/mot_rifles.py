from mw2.context.mod_creation import ModCreationContext
from script.mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair
from ._weapons import M16A2, M249, AT4

def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # MOT. RIFLES.
    with ctx.create_infantry_unit("MOT. RIFLES", "US", "Rifles_half_AT4_US", [(M16A2, 6), (M249, 2), (AT4, 1)]) as mot_rifles:
        mot_rifles.modules.ui.UpgradeFromUnit='d9_CMD_MOT_RIFLES_LDR_US'
        mot_rifles.modules.production.command_point_cost = 55
        return mot_rifles