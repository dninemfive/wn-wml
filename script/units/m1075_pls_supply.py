from context.module_context import ModuleContext
from context.unit_registrar import UnitRegistrar
from metadata.division_unit_registry import UnitInfo

def create(ctx: UnitRegistrar) -> UnitInfo | None:
    # M1075 PLS
    # copy of: HEMTT
    with ctx.create_unit("M1075 PLS SUPPLY", "US", "HEMTT_US") as m1075_pls:
        # todo: get this as a reference to the unit directly
        m1075_pls.edit_ui_module(UpgradeFromUnit="Descriptor_Unit_d9_M998_HUMVEE_SUPPLY_US")
        return UnitInfo(m1075_pls, 1, [0, 3, 2, 0])