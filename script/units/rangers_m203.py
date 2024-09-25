from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
from units._utils import edit_standard_squad


def create(ctx: ModCreationContext) -> UnitRules | None:
    # RANGERS (M203)
    with ctx.create_unit("MOT. RIFLES", "US", "Ranger_US") as rangers_m203:
        # weapons:
        # - Colt Commando x4
        # - M16A2 x3 (squad leader + 2 grenadier)
        # - SAW x2
        # - M203 x2 w/ 36rd each
        # edit WeaponDescriptor:
        #   insert M16A2 into slot 1
        #   create M203 ammo
        #   append M203 to weapons
        # make custom showroom unit
        rangers_m203.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_Ranger_Dragon_US')
        return UnitRules(rangers_m203, 2, [0, 6, 4, 0])