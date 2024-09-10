from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.division_unit_registry import UnitInfo

def create(ctx: UnitCreationContext) -> UnitInfo | None:
    # M998 HUMVEE SUPPLY
    #   copy of: M35 Supply
    with ctx.create_unit("M998 HUMVEE SQC.", "US", "M1038_Humvee_US") as m998_humvee_sqc:
        with ModuleContext(m998_humvee_sqc.unit_object, "TUnitUIModuleDescriptor") as ui_module:
            # TUnitUIModuleDescriptor/UpgradeFromUnit cleared
            ui_module.object.remove_by_member("UpgradeFromUnit")
    # transports don't get added to divisions separately
    return None