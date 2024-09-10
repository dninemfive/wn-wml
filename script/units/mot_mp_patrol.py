from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.deck_unit_info import UnitInfo
from misc.unit_creator import UNIT_UI
from ndf_parse.model import List

def create(ctx: UnitCreationContext) -> UnitInfo | None:
    # MOT. MP PATROL
    # (just copy AB MP PATROL)
    with ctx.create_unit("MOT. MP PATROL", "US", "Airborne_MP_US") as mp_patrol:
        with mp_patrol.module_context(UNIT_UI) as ui_module:
            specialties: List = ui_module.object.by_member("SpecialtiesList").value
            specialties.remove(specialties.find_by_cond(lambda x: x.value == "'_para'"))
            ui_module.edit_members(SpecialtiesList=specialties)
        mp_patrol.remove_module("TDeploymentShiftModuleDescriptor")
        return UnitInfo(mp_patrol, 2, [0, 6, 4, 0], ["$/GFX/Unit/Descriptor_Unit_d9_M998_HUMVEE_SQC_US", "$/GFX/Unit/Descriptor_Unit_M1025_Humvee_MP_US"])
        