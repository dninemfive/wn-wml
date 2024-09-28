from script.context.mod_creation import ModCreationContext
from script.context.unit_module import UnitModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
from units._utils import edit_standard_squad
from units._weapons import COLT_COMMANDO, M16A2, M249, M203
from script.creators.unit.infantry import InfantryUnitCreator

def create(ctx: ModCreationContext) -> UnitRules | None:
    # RANGERS (M203)
    with ctx.create_unit("RANGERS (M203)", "US", "Ranger_US") as rangers_m203:
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
        squad: InfantryUnitCreator = InfantryUnitCreator.copy_parent(ctx.guids, rangers_m203, 'US', (COLT_COMMANDO, 4), (M16A2, 3), (M249, 2), (M203, 2))
        squad.apply(ctx.ndf, rangers_m203.msg)
        squad.edit_unit(rangers_m203)
        rangers_m203.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_Ranger_Dragon_US')
        return UnitRules(rangers_m203, 2, [0, 6, 4, 0])