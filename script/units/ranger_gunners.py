from context.mod_creation import ModCreationContext
from metadata.division_unit_registry import UnitRules
from units._weapons import M16A2, M60E3

def create(ctx: ModCreationContext) -> UnitRules | None:
    # RANGER GUNNERS
    with ctx.create_infantry_unit("RANGER GUNNERS", "US", "Ranger_US", [(M16A2, 7), (M60E3, 1), (M60E3, 1), (M60E3, 1)]) as ranger_gunners:
        ranger_gunners.UpgradeFromUnit = 'Airborne_HMG_US'
        return UnitRules(ranger_gunners, 2, [0, 6, 4, 0])