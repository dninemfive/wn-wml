from context.mod_creation import ModCreationContext
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
from creators.unit.basic import UNIT_UI
import utils.ndf.unit_module as module
import utils.ndf.edit as edit

def create(ctx: ModCreationContext) -> UnitRules | None:
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
        return UnitRules(mot_mp, 2, [0, 6, 4, 0], ["$/GFX/Unit/Descriptor_Unit_M1025_Humvee_MP_US"])
        