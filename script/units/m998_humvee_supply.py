from constants.ndf_paths import UNITE_DESCRIPTOR
from context.mod_creation import ModCreationContext
from context.unit_module import UnitModuleContext
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List, Object

from creators.unit.basic import BasicUnitCreator
from wrappers.unit import UnitWrapper

MODULES_DESCRIPTORS = "ModulesDescriptors"

# todo: put most of this structure in an @annotation
def create(ctx: ModCreationContext) -> UnitRules | None:
    # M998 HUMVEE SUPPLY
    #   copy of: M35 Supply
    with ctx.create_unit("M998 HUMVEE SUPPLY", "US", "M35_supply_US") as m998_humvee_supply:
        # TODO: will need to replace showroom unit somehow. Maybe set the M1038 Humvee as the base and then add supply module to it?
        # need to have a way to just do (unit).MakeSupply, (unit).MakeNotTransport, &c
        edit_with_m1038(m998_humvee_supply, ctx.get_unit("M1038_Humvee_US"))
        edit_with_rover101fc(m998_humvee_supply, ctx.get_unit("Rover_101FC_supply_UK"))
        m998_humvee_supply.modules.ui.edit_members(
            # upgrade from M561 SUPPLY GOAT
            UpgradeFromUnit='Gama_Goat_supply_US',
            # TODO: automate this as part of copying the appearance of another unit?
            ButtonTexture='M1038_Humvee_US'
        )
        # make M35 upgrade from this instead
        ctx.get_unit('M35_supply_US').modules.ui.UpgradeFromUnit = m998_humvee_supply
        # TODO: make stealth mediocre? see M561 SUPPLY GOAT
        return UnitRules(m998_humvee_supply, 2, [10, 8, 6, 4])

def edit_with_m1038(m998_humvee_supply: BasicUnitCreator, m1038_humvee: UnitWrapper) -> None:
    m998_humvee_supply.modules.replace_from(m1038_humvee, 'ApparenceModel', by_name=True)
    m998_humvee_supply.modules.replace_from(m1038_humvee, 'GenericMovement', by_name=True)
    m998_humvee_supply.modules.replace_from(m1038_humvee, 'LandMovement', by_name=True)
    m998_humvee_supply.modules.replace_from(m1038_humvee, 'TBaseDamageModuleDescriptor')

def edit_with_rover101fc(m998_humvee_supply: BasicUnitCreator, rover_101fc_supply: UnitWrapper) -> None:
    m998_humvee_supply.modules.replace_from(rover_101fc_supply, 'TSupplyModuleDescriptor')
    m998_humvee_supply.modules.production.command_point_cost\
         = rover_101fc_supply.modules.production.command_point_cost