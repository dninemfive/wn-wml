from context.module_context import ModuleContext
from script.context.unit_id_manager import UnitIdManager
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from script.creators.unit import UNIT_UI
from ndf_parse.model import List, ListRow
from utils.ndf import to_List as qlist

def create(ctx: UnitIdManager) -> UnitRules | None:
    # M998 AVENGER
    # copy AB M998 AVENGER
    with ctx.create_unit("M998 Avenger", "US", "M998_Avenger_US") as m998_avenger:
        # remove forward deploy
        m998_avenger.remove_module("TDeploymentShiftModuleDescriptor")
        # remove para trait
        m998_avenger.edit_ui_module(SpecialtiesList=qlist("'AA'"))
        # TODO: maybe allow deployment via CH-47D?
        return UnitRules(m998_avenger, 2, [0, 4, 3, 0])
        