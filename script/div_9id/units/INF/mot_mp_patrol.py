from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair
from ndf_parse.model import List


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # MOT. MP PATROL
    # (just copy AB MP PATROL)
    with ctx.create_unit("MOT. MP PATROL", "US", "Airborne_MP_US") as mot_mp:
        mot_mp.modules.ui.edit_members(
            ButtonTexture='MP_US',
            UpgradeFromUnit='MP_US'
        )
        mot_mp.modules.ui.SpecialtiesList.remove('_para')
        mot_mp.modules.remove("TDeploymentShiftModuleDescriptor")
        # same cost as normal MPs, not AB MPs
        mot_mp.modules.production.command_point_cost = ctx.get_unit('MP_US').modules.production.command_point_cost
        ctx.get_unit('MP_RCL_US').modules.ui.UpgradeFromUnit = mot_mp
        return mot_mp
        