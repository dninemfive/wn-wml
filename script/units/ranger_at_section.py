from context.mod_creation import ModCreationContext
from metadata.division_unit_registry import UnitRules
from units._weapons import M16A2

def create(ctx: ModCreationContext) -> UnitRules | None:
    # RANGER AT SECTION
    # weapons:
    # - M16A2 x10
    # - M67 90mm
    # - M67 90mm
    # - M67 90mm
    with ctx.create_infantry_unit("RANGER AT SECTION", "US", "Ranger_US", [(M16A2, 10)]) as rangers_m67:
        rangers_m67.UpgradeFromUnit = 'd9_RANGERS_M203_US'
        return UnitRules(rangers_m67, 2, [0, 6, 4, 0])