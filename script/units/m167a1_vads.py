from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.division_unit_registry import UnitInfo
from metadata.unit import UnitMetadata
from misc.unit_creator import UNIT_UI
from ndf_parse.model import List, ListRow
from utils.ndf import to_List as qlist

def create(ctx: UnitCreationContext) -> UnitInfo | None:
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
        # update ttransportablemoduledescriptor (TODO: automate)
        return UnitInfo(m167a1_vads, 2, [0, 4, 3, 0])
        