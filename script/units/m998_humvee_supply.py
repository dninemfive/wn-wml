from constants.ndf_paths import UNITE_DESCRIPTOR
from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List, Object

from creators.unit import UnitCreator

MODULES_DESCRIPTORS = "ModulesDescriptors"

# todo: put most of this structure in an @annotation
def create(ctx: ModCreationContext) -> UnitRules | None:
    # M998 HUMVEE SUPPLY
    #   copy of: M35 Supply
    with ctx.create_unit("M998 HUMVEE SUPPLY", "US", "M35_supply_US", "M1038_Humvee_US") as m998_humvee_supply:
        edit_with_m1038(m998_humvee_supply, m998_humvee_supply.get_other_unit("M1038_Humvee_US"))
        edit_with_rover101fc(m998_humvee_supply, m998_humvee_supply.get_other_unit("Rover_101FC_supply_UK"))
        with ModuleContext(m998_humvee_supply.unit_object, "TUnitUIModuleDescriptor") as ui_module:
            # TUnitUIModuleDescriptor/UpgradeFromUnit cleared
            ui_module.object.remove_by_member("UpgradeFromUnit")
        # TODO: make stealth mediocre? see M561 SUPPLY GOAT
        return UnitRules(m998_humvee_supply, 2, [10, 8, 6, 4])

def edit_with_m1038(m998_humvee_supply: UnitCreator, m1038_humvee: Object) -> None:
    # ApparenceModel replaced with that of M1038 Humvee
    m998_humvee_supply.replace_module_from(m1038_humvee, 'ApparenceModel', by_name=True)
    # GenericMovement replaced with that of M1038 Humvee
    m998_humvee_supply.replace_module_from(m1038_humvee, 'GenericMovement', by_name=True)
    # LandMovement replaced with that of M1038 Humvee
    m998_humvee_supply.replace_module_from(m1038_humvee, 'LandMovement', by_name=True)
    # TBaseDamageModuleDescriptor replaced with that of M1038 Humvee
    m998_humvee_supply.replace_module_from(m1038_humvee, 'TBaseDamageModuleDescriptor')

def edit_with_rover101fc(m998_humvee_supply: UnitCreator, rover_101fc_supply: Object) -> None:
    # TSupplyModuleDescriptor replaced with that of Rover 101FC Supply
    m998_humvee_supply.replace_module_from(rover_101fc_supply, 'TSupplyModuleDescriptor')
    # TProductionModuleDescriptor/ProductionResourcesNeeded replaced with that of Rover 101FC Supply
    m998_humvee_supply.replace_module_from(rover_101fc_supply, 'TProductionModuleDescriptor')
    pass