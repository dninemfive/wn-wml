from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
from model.squads.infantry_weapon_set import InfantryWeaponSet
from model.squads.squad import Squad
import utils.ndf.edit as edit
from units._utils import edit_standard_squad
from units._weapons import M16A2, M249, DRAGON


def create(ctx: ModCreationContext) -> UnitRules | None:
    # MOT. RIFLES.
    with ctx.create_unit("MOT. RIFLES (DRAGON)", "US", "Rifles_half_Dragon_US") as mot_rifles_dragon:
        weapons = InfantryWeaponSet((M16A2, 7), (M249, 2), (DRAGON, 1))
        squad: Squad = Squad.from_weapon_set(ctx.guids, mot_rifles_dragon.new, 'US', (0, 10), 'Rifles_US', weapons)
        squad.apply(ctx.ndf, mot_rifles_dragon.msg)
        squad.edit_unit(mot_rifles_dragon)
        # make custom showroom unit
        mot_rifles_dragon.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_d9_MOT_RIFLES_US')
        mot_rifles_dragon.CommandPointCost = 65
        return UnitRules(mot_rifles_dragon, 2, [0, 6, 4, 0])