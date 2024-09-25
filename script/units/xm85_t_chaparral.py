from context.mod_creation_context import ModCreationContext
from metadata.unit_rules import UnitRules
import utils.ndf.edit as edit
import utils.ndf.unit_module as module

def create(ctx: ModCreationContext) -> UnitRules | None:
    # MIM-72A T-CHAPARRAL
    # copy RAPIER FSA
    with ctx.create_unit("XM-85 T-CHAPARRAL", "US", "DCA_Rapier_FSA_UK", button_texture_src_path='img/units/xm85_t_chaparral/icon.png') as t_chap:
        # replace weapon with M48A1 CHAPARRAL
        t_chap.replace_module_from('M48_Chaparral_MIM72F_US', 'WeaponManager', by_name=True)
        with t_chap.edit_weapons() as weapons:
            weapons.Salves = [1]
            edit.members(weapons.get_turret_weapon(0),
                         Ammunition=f'$/GFX/Weapon/Ammo_SAM_MIM72F')
        # make M48A1 CHAPARRAL upgrade from this
        m48_chap = t_chap.get_other_unit('M48_Chaparral_MIM72F_US')
        edit.members(module.get(m48_chap, 'TUnitUIModuleDescriptor'), UpgradeFromUnit=t_chap.new.descriptor_name)
        # set country to US
        with t_chap.module_context('TUnitUIModuleDescriptor') as ui_module:
            ui_module.remove_member('UpgradeFromUnit')
            ui_module.edit_members(CountryTexture="'CommonTexture_MotherCountryFlag_US'")
        # advanced: replace british dude models with US dude models
        return UnitRules(t_chap, 2, [0, 4, 3, 0])