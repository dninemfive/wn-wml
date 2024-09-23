from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
from units._utils import make_standard_squad_module


def create(ctx: ModCreationContext) -> UnitRules | None:
    # MOT. RIFLES.
    with ctx.create_unit("MOT. RIFLES", "US", "Rifles_half_AT4_US") as mot_rifles:
        # change squad count from 6 to 9        
        edit_standard_squad(mot_rifles, 7, 2, 26, 92)
        # make custom showroom unit
        mot_rifles.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_d9_CMD_MOT_RIFLES_LDR_US')
        return UnitRules(mot_rifles, 2, [0, 6, 4, 0])
        
def edit_standard_squad(squad: UnitCreator, num_rifles: int, num_SAWs: int, salvos_per_rifle: int, salvos_per_SAW: int) -> None:
    with squad.edit_weapons() as weapons:
        weapons.edit_members(Salves=[salvos_per_rifle*num_rifles,salvos_per_SAW*num_SAWs,4])
        edit.members(weapons.get_turret_weapon(0,0), NbWeapons=num_rifles)
        edit.members(weapons.get_turret_weapon(1,0), NbWeapons=num_SAWs)
    squad_size = num_rifles + num_SAWs
    with squad.module_context('TBaseDamageModuleDescriptor') as damage_module:
        damage_module.edit_members(MaxPhysicalDamages=squad_size)
    with squad.module_context('GroupeCombat', by_name=True) as groupe_combat:
        edit.members(groupe_combat.object.by_member('Default').value, NbSoldatInGroupeCombat=squad_size)
    squad.replace_module('TInfantrySquadWeaponAssignmentModuleDescriptor', make_standard_squad_module(squad_size, num_SAWs))
    with squad.module_context('TTacticalLabelModuleDescriptor') as label_module:
        label_module.edit_members(NbSoldiers=squad_size)
        # todo: edit bounding box size?