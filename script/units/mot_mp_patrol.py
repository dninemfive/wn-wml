from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.unit_module as module
import utils.ndf.edit as edit

def create(ctx: ModCreationContext) -> UnitRules | None:
    # MOT. MP PATROL
    # (just copy AB MP PATROL)
    with ctx.create_unit("MOT. MP PATROL", "US", "Airborne_MP_US") as mp_patrol:
        with mp_patrol.module_context(UNIT_UI) as ui_module:
            specialties: List = ui_module.object.by_member("SpecialtiesList").value
            specialties.remove(specialties.find_by_cond(lambda x: x.value == "'_para'"))
            ui_module.edit_members(SpecialtiesList=specialties,
                                   ButtonTexture="'Texture_Button_Unit_MP_US'",
                                   UpgradeFromUnit='Descriptor_Unit_MP_US')
        mp_patrol.remove_module("TDeploymentShiftModuleDescriptor")
        mp_patrol_vanilla = mp_patrol.get_other_unit('MP_US')
        # same cost as normal MPs, not AB MPs
        with mp_patrol.module_context('TProductionModuleDescriptor') as production_module:
            production_module.object\
                             .by_member('ProductionRessourcesNeeded').value\
                             .by_key('$/GFX/Resources/Resource_CommandPoints').value\
                = module.get(mp_patrol_vanilla, 'TProductionModuleDescriptor')\
                             .by_member('ProductionRessourcesNeeded').value\
                             .by_key('$/GFX/Resources/Resource_CommandPoints').value
        mp_rcl = mp_patrol.get_other_unit('MP_RCL_US')
        edit.members(module.get(mp_rcl, 'TUnitUIModuleDescriptor'), UpgradeFromUnit='Descriptor_Unit_d9_MOT_MP_PATROL_US')
        return UnitRules(mp_patrol, 2, [0, 6, 4, 0], ["$/GFX/Unit/Descriptor_Unit_M1025_Humvee_MP_US"])
        