from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.deck_unit_info import TDeckUniteRule
from misc.unit_creator import UNIT_UI
from ndf_parse.model import List, ListRow
from units.util import make_unit_rule
from utils.ndf import list_to_List as qlist

def create(ctx: UnitCreationContext) -> tuple[tuple[str, int], TDeckUniteRule]:
    # M998 AVENGER
    # copy AB M998 AVENGER
    with ctx.create_unit("M998 Avenger", "US", "M998_Avenger_US") as m998_avenger:
        # remove forward deploy
        m998_avenger.remove_module("TDeploymentShiftModuleDescriptor")
        # remove para trait
        m998_avenger.edit_ui_module(SpecialtiesList=qlist("'AA'"))
        return make_unit_rule(m998_avenger.new, [0, 4, 3, 0], 2)
        