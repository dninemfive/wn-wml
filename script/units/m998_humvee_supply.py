from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.deck_unit_info import UnitInfo
from units.util import make_unit_rule

# todo: put most of this structure in an @annotation
def create(ctx: UnitCreationContext) -> UnitInfo | None:
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
            return UnitInfo(m998_humvee_supply, 2, [10, 8, 6, 4])