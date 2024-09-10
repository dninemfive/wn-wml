from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.deck_unit_info import TDeckUniteRule
from units.util import make_unit_rule

def create(ctx: UnitCreationContext) -> tuple[tuple[str, int], TDeckUniteRule]:
    # M1075 PLS
    # copy of: HEMTT
    with ctx.create_unit("M1075 PLS SUPPLY", "US", "HEMTT_US") as m1075_pls:
        # todo: get this as a reference to the unit directly
        m1075_pls.edit_ui_module(UpgradeFromUnit="Descriptor_Unit_d9_M998_HUMVEE_SUPPLY_US")
        return make_unit_rule(m1075_pls, [0, 3, 2, 0], 1)