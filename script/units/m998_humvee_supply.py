from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.deck_unit_info import TDeckUniteRule
from units.util import make_unit_rule

# todo: put most of this structure in an @annotation
def create(ctx: UnitCreationContext) -> tuple[tuple[str, int], TDeckUniteRule]:
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
            return make_unit_rule(m998_humvee_supply.new, [10, 8, 6, 4], 2)