from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # 👓 FAV M2HB
    # model: ILTIS HMG
    # range: custom
    # air transportable
    with ctx.create_unit("#RECO1 FAV M2HB", "US", "Iltis_HMG_BEL") as fav_m2hb:
        fav_m2hb.modules.type.edit_members(
            MotherCountry='US'                             # TODO: set this, icon flag, &c with one item
        )
        fav_m2hb.command_point_cost = 45
        fav_m2hb.modules.ui.edit_members(
            SpecialtiesList=['reco', 'air_transportable']
        )
        fav_m2hb.modules.remove('Transporter', by_name=True)
        return (fav_m2hb, 'Ferret_Mk2_UK')