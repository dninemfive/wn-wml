from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
import utils.ndf.unit_module as module
from units._utils import edit_standard_squad


def create(ctx: ModCreationContext) -> UnitRules | None:
    # FOLT
    with ctx.create_unit("#RECO2 FOLT", "US", "Scout_US") as folt:
        # 2 guys
        # both with M16s
        # set MG to M249
        with folt.edit_weapons() as weapons:
            edit.members(weapons.get_turret_weapon(1, 0), Ammunition='$/GFX/Weapon/Ammo_SAW_M249_5_56mm', EffectTag="'FireEffect_SAW_M249_5_56mm'")
        # make custom showroom unit
        # upgradfe from... something
        return UnitRules(folt, 3, [0, 6, 4, 0])