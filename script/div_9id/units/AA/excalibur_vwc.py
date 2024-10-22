from mw2.context.mod_creation import ModCreationContext
from ndf_parse.model import List, ListRow

from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    with ctx.create_unit("EXCALIBUR VWC", "US", "VLRA_20mm_FR") as excalibur:
        excalibur.modules.remove("TDeploymentShiftModuleDescriptor")
        excalibur.modules.ui.SpecialtiesList.remove('_para')
        excalibur.modules.ui.UpgradeFromUnit = 'DCA_M167A2_Vulcan_20mm_Aero_US'
        excalibur.command_point_cost = 100
        excalibur.modules.weapon_manager.Default = 'DCA_M167A2_Vulcan_20mm_Aero_US'
        excalibur.unit.set_country('US')
        return excalibur
        