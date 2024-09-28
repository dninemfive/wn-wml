from script.context.mod_creation import ModCreationContext
from metadata.division_unit_registry import UnitRules
from script.creators.unit.infantry import InfantryUnitCreator
from units._weapons import M16A2, M249, DRAGON


def create(ctx: ModCreationContext) -> UnitRules | None:
    # MOT. RIFLES (DRAGON)
    with ctx.create_infantry_unit("MOT. RIFLES (DRAGON)", "US", "Rifles_half_Dragon_US", [(M16A2, 7), (M249, 2), (DRAGON, 1)]) as mot_rifles_dragon:
        mot_rifles_dragon.UpgradeFromUnit='d9_MOT_RIFLES_US'
        mot_rifles_dragon.CommandPointCost = 65
        return UnitRules(mot_rifles_dragon, 2, [0, 6, 4, 0])