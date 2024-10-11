from context.mod_creation import ModCreationContext
from context.unit_module import UnitModuleContext
from creators.unit.basic import UNIT_UI
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List


def create(ctx: ModCreationContext) -> UnitRules | None:
    # Mk.19 40mm
    with ctx.create_unit("Mk.19 40mm", "US", "HMGteam_Mk19_AB_US") as mk19:
        mk19.modules.ui.SpecialtiesList.remove('_para')
        mk19.modules.ui.UpgradeFromUnit='HMGteam_'
        mk19.modules.remove("HMGteam_M2HB_US")
        # TODO: change depiction to use non-AB models
        return UnitRules(mk19, 1, [0, 6, 4, 0])
        