from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.deck_unit_info import TDeckUniteRule
from units.util import make_unit_rule

def create(ctx: UnitCreationContext) -> tuple[tuple[str, int], TDeckUniteRule] | None:
    # M998 HUMVEE SUPPLY
    #   copy of: M35 Supply
    with ctx.create_unit("M998 HUMVEE SQC.", "US", "M1038_Humvee_US") as m998_humvee_sqc:
        with ModuleContext(m998_humvee_sqc.unit_object, "TUnitUIModuleDescriptor") as ui_module:
            # TUnitUIModuleDescriptor/UpgradeFromUnit cleared
            ui_module.object.remove_by_member("UpgradeFromUnit")
    # transports don't get added to divisions separately
    return None