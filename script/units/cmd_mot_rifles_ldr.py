from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
from units._utils import make_standard_squad_module


def create(ctx: ModCreationContext) -> UnitRules | None:
    # CMD MOT. RIFLES LDR.
    with ctx.create_unit("#CMD MOT. RIFLES LDR.", "US", "LightRifles_CMD_US") as mot_rifles_ldr:
        # change squad count from 6 to 8
        # change LAW from M72A3 to AT-4
        #   change in weapons thingy
        with mot_rifles_ldr.edit_weapons('WeaponDescriptor_Rifles_half_AT4_US') as weapons:
            weapons.edit_members(Salves=[26*6, 92*2, 4])
            edit.members(weapons.get_turret_weapon(0, 0), NbWeapons=6)
        #   change in models - make custom Gfx thing with custom AllWeaponsSubdepiction_xx_US
        #       or maybe i can just steal it from a unit with the appropriate weapons? i.e. FIRE TEAM (AT-4)
        with mot_rifles_ldr.module_context('ApparenceModel', by_name=True) as apparence_module:
            apparence_module.edit_members(Depiction='~/Gfx_Rifles_half_AT4_US')
        with mot_rifles_ldr.module_context('TBaseDamageModuleDescriptor') as damage_module:
            damage_module.edit_members(MaxPhysicalDamages=8)
        with mot_rifles_ldr.module_context('GroupeCombat', by_name=True) as groupe_combat:
            # TODO: edit MimeticName, UnitFXKey?
            edit.members(groupe_combat.object.by_member('Default').value, NbSoldatInGroupeCombat=8)
        mot_rifles_ldr.replace_module('TInfantrySquadWeaponAssignmentModuleDescriptor', make_standard_squad_module(8, 2))
        with mot_rifles_ldr.module_context('TTacticalLabelModuleDescriptor') as label_module:
            label_module.edit_members(NbSoldiers=8)
        # make custom showroom unit
        return UnitRules(mot_rifles_ldr, 2, [0, 6, 4, 0])
        