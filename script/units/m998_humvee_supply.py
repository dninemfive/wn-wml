from constants.ndf_paths import UNITE_DESCRIPTOR
from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List, Object

MODULES_DESCRIPTORS = "ModulesDescriptors"

# todo: put most of this structure in an @annotation
def create(ctx: ModCreationContext) -> UnitRules | None:
    # M998 HUMVEE SUPPLY
    #   copy of: M35 Supply
    with ctx.create_unit("M998 HUMVEE SUPPLY", "US", "M35_supply_US") as m998_humvee_supply:
        m1038_humvee_modules: List = ctx.ndf[UNITE_DESCRIPTOR].by_name("Descriptor_Unit_M1038_Humvee_US").value.by_member(MODULES_DESCRIPTORS).value
        # ApparenceModel replaced with that of M1038 Humvee
        apparence_model: Object = m1038_humvee_modules.by_name("ApparenceModel").value.copy()
        m998_humvee_supply.get_module_by_name("ApparenceModel").value = apparence_model
        # GenericMovement replaced with that of M1038 Humvee
        # LandMovement replaced with that of M1038 Humvee
        # TBaseDamageModuleDescriptor replaced with that of M1038 Humvee
        # TSupplyModuleDescriptor replaced with that of Rover 101FC Supply
        # TProductionModuleDescriptor/ProductionResourcesNeeded replaced with that of Rover 101FC Supply
        with ModuleContext(m998_humvee_supply.unit_object, "TUnitUIModuleDescriptor") as ui_module:
            # TUnitUIModuleDescriptor/UpgradeFromUnit cleared
            ui_module.object.remove_by_member("UpgradeFromUnit")
        return UnitRules(m998_humvee_supply, 2, [10, 8, 6, 4])
