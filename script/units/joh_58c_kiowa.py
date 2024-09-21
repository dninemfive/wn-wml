from context.mod_creation_context import ModCreationContext
from metadata.unit_rules import UnitRules


def create(ctx: ModCreationContext) -> UnitRules | None:
    # JOH-58C Kiowa
    # Copy of: OH-58C/S
    with ctx.create_unit("JOH-58C KIOWA", "US", "OH58_CS_US") as joh_58c_kiowa:
        # reduce stinger count
        # add minigun
        # adjust missile carriage?
        return UnitRules(joh_58c_kiowa, 2, [0, 4, 3, 0])
        