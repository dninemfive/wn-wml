
from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair
from ndf_parse.model import List, ListRow, Object


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # M998 HUMVEE GLH-L
    with ctx.create_unit("M998 HUMVEE GLH-L", "US", "M1025_Humvee_TOW_US") as m998_humvee_glhl:
        with m998_humvee_glhl.edit_weapons('M1025_Humvee_TOW_US') as weapons:
            weapons.edit_members(Salves=[4,])
            weapons.get_turret_weapon(0).by_member('Ammunition').value = 'Ammo_AGM_AGM114A_x2_sol'
        m998_humvee_glhl.modules.ui.UpgradeFromUnit='M1025_Humvee_TOW_para_US'
        return m998_humvee_glhl