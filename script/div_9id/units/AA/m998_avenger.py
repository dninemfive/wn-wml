from mw2.context.mod_creation import ModCreationContext
from ndf_parse.model import List, ListRow

from script.mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # M998 AVENGER
    # copy AB M998 AVENGER
    with ctx.create_unit("M998 Avenger", "US", "M998_Avenger_US") as m998_avenger:
        # remove forward deploy
        m998_avenger.modules.remove("TDeploymentShiftModuleDescriptor")
        # remove para trait
        m998_avenger.modules.ui.SpecialtiesList.remove('_para')
        m998_avenger.modules.ui.UpgradeFromUnit = 'M48_Chaparral_MIM72F_US'
        m998_avenger.command_point_cost -= 5
        # make AB M998 AVENGER upgrade from M998 AVENGER
        ctx.get_unit('M998_Avenger_US').modules.ui.UpgradeFromUnit = m998_avenger
        return m998_avenger
        