from context.mod_creation import ModCreationContext
from metadata.division_unit_registry import UnitRules
from units._weapons import M16A2, M240


def create(ctx: ModCreationContext) -> UnitRules | None:
    # CMD MOT. RIFLES LDR.
    with ctx.create_infantry_unit("#CMD MOT. RIFLES LDR.", "US", "Rifles_CMD_US", [(M16A2, 5), (M240, 1)]) as mot_rifles_ldr:
        return UnitRules(mot_rifles_ldr, 2, [0, 6, 4, 0])
        