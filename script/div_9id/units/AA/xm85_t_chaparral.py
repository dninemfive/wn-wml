from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair
from mw2.utils.ndf import edit


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # XM-85 T-CHAPARRAL
    # copy RAPIER FSA
    with ctx.create_unit("XM-85 T-CHAPARRAL", "US", "DCA_Rapier_FSA_UK",
                         button_texture_src_path='img/units/xm85_t_chaparral/icon.png') as t_chap:
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
        return t_chap