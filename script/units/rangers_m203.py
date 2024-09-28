from context.mod_creation import ModCreationContext
from metadata.division_unit_registry import UnitRules
from units._weapons import COLT_COMMANDO, M16A2, M249, M203

def create(ctx: ModCreationContext) -> UnitRules | None:
    # RANGERS (M203)
    # weapons:
    # - Colt Commando x4
    # - M16A2 x3 (squad leader + 2 grenadier)
    # - SAW x2
    # - M203 x2 w/ 36rd each
    with ctx.create_infantry_unit("RANGERS (M203)", "US", "Ranger_US", [(COLT_COMMANDO, 4), (M16A2, 3), (M249, 2), (M203, 2)]) as rangers_m203:
        rangers_m203.UpgradeFromUnit = 'Ranger_Dragon_US'
        return UnitRules(rangers_m203, 2, [0, 6, 4, 0])