from context.mod_creation import ModCreationContext
from metadata.division_unit_registry import UnitRules
from units._weapons import M16A2


def create(ctx: ModCreationContext) -> UnitRules | None:
    # M224 60mm
    # weapons:
    # - M16A2 x6
    # - M224 60mm x2
    with ctx.create_infantry_unit("M224 60mm", "US", "Rifles_HMG_US", [(M16A2, 6)]) as m224_60mm:
        m224_60mm.UpgradeFromUnit = 'd9_Mk19_40mm_US'
        return UnitRules(m224_60mm, 2, [0, 6, 4, 0])