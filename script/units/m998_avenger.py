from context.module_context import ModuleContext
from context.unit_registrar import UnitRegistrar
from metadata.division_unit_registry import UnitInfo
from metadata.unit import UnitMetadata
from misc.unit_creator import UNIT_UI
from ndf_parse.model import List, ListRow
from utils.ndf import to_List as qlist

def create(ctx: UnitRegistrar) -> UnitInfo | None:
    # M998 AVENGER
    # copy AB M998 AVENGER
    with ctx.create_unit("M998 Avenger", "US", "M998_Avenger_US") as m998_avenger:
        # remove forward deploy
        m998_avenger.remove_module("TDeploymentShiftModuleDescriptor")
        # remove para trait
        m998_avenger.edit_ui_module(SpecialtiesList=qlist("'AA'"))
        # TODO: maybe allow deployment via CH-47D?
        return UnitInfo(m998_avenger, 2, [0, 4, 3, 0])
        