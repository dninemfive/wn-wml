from context.mod_creation import ModCreationContext
from metadata.division_unit_registry import UnitRules
from units._weapons import M16A2, M249, AT4


def create(ctx: ModCreationContext) -> UnitRules | None:
    # OPERATIONAL SUPPORT
    # TODO: change weapon loadout, maybe including M82?
    with ctx.create_infantry_unit("#RECO1 OPERATIONAL SUPPORT", "US", "Scout_US", [(M16A2, 8), (M249, 4), (AT4, 2)]) as op_support:
        # TODO: increase menace
        # TODO: reduce vision
        return UnitRules(op_support, 3, [0, 6, 4, 0])