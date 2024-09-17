from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from metadata.unit import UnitMetadata
from metadata.unit_rules import UnitRules
from ndf_parse.model import List, ListRow
from utils.ndf import to_List as qlist


def create(ctx: ModCreationContext) -> UnitRules | None:
    # M167A1 VADS 20mm
    # copy AB version
    with ctx.create_unit("M167A1 VADS 20mm", "US", "DCA_M167_Vulcan_20mm_US") as m167a1_vads:
        # remove forward-deploy
        m167a1_vads.remove_module("TDeploymentShiftModuleDescriptor")
        # add air-transportable trait
        m167a1_vads.edit_ui_module(SpecialtiesList=qlist("'AA'", "'_canBeAirlifted'"))
        # ensure air-transportable with transportation module
        # add "CanBeAirlifted" to tags
        m167a1_vads.add_tags('"CanBeAirlifted"')
        # advanced: replace soldiers manning it with normal instead of airborne models
        # advanced: insert before AB M167A1 VADS 20mm
        # update ttransportablemoduledescriptor
        return UnitRules(m167a1_vads, 2, [0, 4, 3, 0])
        