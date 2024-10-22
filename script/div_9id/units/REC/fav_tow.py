from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # 👓 FAV TOW
    with ctx.create_unit("#RECO1 FAV TOW", "US", "Iltis_MILAN_BEL") as fav_tow:
        fav_tow.unit.set_country('US')
        fav_tow.command_point_cost = 60
        # TODO: weapons: SAW, TOW
        fav_tow.modules.ui.edit_members(
            SpecialtiesList=['reco', 'air_transportable']
        )
        fav_tow.modules.production.Factory ='Recons'
        fav_tow.modules.ui.UpgradeFromUnit = 'd9_RECO1_FAV_AGL_US'
        return (fav_tow, 'FV721_Fox_UK')