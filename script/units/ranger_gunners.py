from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
from units._utils import edit_standard_squad


def create(ctx: ModCreationContext) -> UnitRules | None:
    # RANGER GUNNERS
    with ctx.create_unit("RANGER GUNNERS", "US", "Ranger_US") as rangers_m203:
        # change squad count to 10
        # weapons:
        # - Colt Commando x7
        # - M60E3
        # - M60E3
        # - M60E3
        # create M60E3 def
        # edit WeaponDescriptor:
        #   replace slot 1 with M60E3
        #   replace slot 2 with M60E3
        #   append M60E3 to weapons
        # make custom showroom unit
        rangers_m203.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_Airborne_HMG_US')
        return UnitRules(rangers_m203, 2, [0, 6, 4, 0])