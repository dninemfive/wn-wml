from context.mod_creation import ModCreationContext
from metadata.unit_rules import UnitRules
import utils.ndf.edit as edit
import utils.ndf.unit_module as module

def create(ctx: ModCreationContext) -> UnitRules | None:
    # MIM-72A T-CHAPARRAL
    # copy RAPIER FSA
    with ctx.create_unit("XM-85 T-CHAPARRAL", "US", "DCA_Rapier_FSA_UK", button_texture_src_path='img/units/xm85_t_chaparral/icon.png') as t_chap:
        # replace weapon with M48A1 CHAPARRAL
        t_chap.modules.replace_from('M48_Chaparral_MIM72F_US', 'WeaponManager', by_name=True)
        with t_chap.edit_weapons() as weapons:
            weapons.Salves = [1]
            edit.members(weapons.get_turret_weapon(0),
                         Ammunition=f'$/GFX/Weapon/Ammo_SAM_MIM72F')
        # make M48A1 CHAPARRAL upgrade from this
        ctx.get_unit('M48_Chaparral_MIM72F_US').modules.ui.UpgradeFromUnit = t_chap
        t_chap.modules.ui.edit_members(
            UpgradeFromUnit=None,
            CountryTexture='US'    
        )
        # advanced: replace british dude models with US dude models
        return UnitRules(t_chap, 2, [0, 4, 3, 0])