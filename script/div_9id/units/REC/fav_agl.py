from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # 👓 FAV AGL
    # model: ILTIS HMG
    # range: custom
    # air transportable
    # weapon: Mk.19 Mod III 40mm
    with ctx.create_unit("#RECO1 FAV AGL", "US", "Iltis_HMG_BEL") as fav_agl:
        fav_agl.modules.type.edit_members(
            MotherCountry='US'                             # TODO: set this, icon flag, &c with one item
        )
        fav_agl.command_point_cost = 45
        fav_agl.modules.ui.edit_members(
            SpecialtiesList=['reco', 'air_transportable'],
            UpgradeFromUnit='d9_RECO1_FAV_M2HB_US'
        )
        fav_agl.modules.remove('Transporter', by_name=True)
        with fav_agl.edit_weapons('M1025_Humvee_AGL_nonPara_US') as _:
            pass
        return (fav_agl, 'Ferret_Mk2_UK')