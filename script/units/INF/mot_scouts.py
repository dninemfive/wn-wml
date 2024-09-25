from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
import utils.ndf.unit_module as module
from units._utils import edit_standard_squad


def create(ctx: ModCreationContext) -> UnitRules | None:
    # MOT. SCOUTS
    with ctx.create_unit("#RECO2 MOT. SCOUTS", "US", "Scout_US") as mot_scouts:
        # set MG to M249
        with mot_scouts.edit_weapons() as weapons:
            edit.members(weapons.get_turret_weapon(1, 0), Ammunition='$/GFX/Weapon/Ammo_SAW_M249_5_56mm', EffectTag="'FireEffect_SAW_M249_5_56mm'")
        # make custom showroom unit
        # insert between scouts and ab scouts
        mot_scouts.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_Scout_US')
        ab_scouts = mot_scouts.get_other_unit('Descriptor_Unit_Airborne_Scout_US')
        edit.members(module.get(ab_scouts, 'TUnitUIModuleDescriptor'), UpgradeFromUnit='Descriptor_Unit_d9_RECO2_MOT_SCOUTS_US')
        # TODO: update appearance to have weapons match
        return UnitRules(mot_scouts, 3, [0, 6, 4, 0])