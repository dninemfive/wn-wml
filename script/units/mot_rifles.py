from context.mod_creation import ModCreationContext
from metadata.division_unit_registry import UnitRules
from units._weapons import M16A2, M249, AT4

def create(ctx: ModCreationContext) -> UnitRules | None:
    # MOT. RIFLES.
    with ctx.create_infantry_unit("MOT. RIFLES", "US", "Rifles_half_AT4_US", [(M16A2, 7), (M249, 2), (AT4, 1)]) as mot_rifles:
        mot_rifles.modules.ui.UpgradeFromUnit='d9_CMD_MOT_RIFLES_LDR_US'
        mot_rifles.modules.production.command_point_cost = 55
        return UnitRules(mot_rifles, 2, [0, 6, 4, 0])