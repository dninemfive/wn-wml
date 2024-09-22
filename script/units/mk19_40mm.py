from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List


def create(ctx: ModCreationContext) -> UnitRules | None:
    # Mk.19 40mm
    with ctx.create_unit("Mk.19 40mm", "US", "HMGteam_Mk19_AB_US") as mk19:
        with mk19.module_context(UNIT_UI) as ui_module:
            specialties: List = ui_module.object.by_member("SpecialtiesList").value
            specialties.remove(specialties.find_by_cond(lambda x: x.value == "'_para'"))
            ui_module.edit_members(SpecialtiesList=specialties,
                                   UpgradeFromUnit='Descriptor_Unit_HMGteam_M2HB_US')
        mk19.remove_module("TDeploymentShiftModuleDescriptor")
        return UnitRules(mk19, 1, [0, 6, 4, 0])
        