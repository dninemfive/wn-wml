from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from metadata.division_unit_registry import UnitRules

# todo: put most of this structure in an @annotation
def create(ctx: ModCreationContext) -> UnitRules | None:
    # M998 HUMVEE SUPPLY
    #   copy of: M35 Supply
    with ctx.create_unit("M998 HUMVEE SUPPLY", "US", "M35_supply_US") as m998_humvee_supply:
        # "UNITE_M35_supply_US" replaced in TTagsModuleDescriptor
        # ApparenceModel replaced with that of M1038 Humvee
        # GenericMovement replaced with that of M998 Humvee
        # LandMovement replaced with that of M998 Humvee
        # TBaseDamageModuleDescriptor replaced with that of M1038 Humvee
        # TSupplyModuleDescriptor replaced with that of Rover 101FC Supply
        # TProductionModuleDescriptor/ProductionResourcesNeeded replaced with that of Rover 101FC Supply
        with ModuleContext(m998_humvee_supply.unit_object, "TUnitUIModuleDescriptor") as ui_module:
            # TUnitUIModuleDescriptor/UpgradeFromUnit cleared
            ui_module.object.remove_by_member("UpgradeFromUnit")
            return UnitRules(m998_humvee_supply, 2, [10, 8, 6, 4])