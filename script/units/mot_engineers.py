import utils.ndf.edit as edit
import utils.ndf.unit_module as module
from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
from units._utils import edit_standard_squad


def create(ctx: ModCreationContext) -> UnitRules | None:
    # MOT. RIFLES.
    with ctx.create_unit("MOT. ENGINEERS", "US", "Engineers_US") as mot_engineers:
        # change squad count from 10 to 8        
        edit_standard_squad(mot_engineers, 6, 2, 26, 92)
        # change MG to M249
        # TODO: allow changing weapons inside of edit_standard_squad
        # with mot_engineers.edit_weapons() as weapons:
        #     edit.members(weapons.get_turret_weapon(1, 0), Ammunition='$/GFX/Weapon/Ammo_SAW_M249_5_56mm', EffectTag="'FireEffect_SAW_M249_5_56mm'")
        # insert between engineers and engineers (FLASH)
        mot_engineers.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_Engineers_US')
        engineers_flash = mot_engineers.get_other_unit('Engineers_Flash_US')
        edit.members(module.get(engineers_flash, 'TUnitUIModuleDescriptor'), UpgradeFromUnit='Descriptor_Unit_d9_MOT_ENGINEERS_US')
        # make custom showroom unit
        return UnitRules(mot_engineers, 2, [0, 6, 4, 0])