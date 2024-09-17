from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.division_unit_registry import UnitInfo
from metadata.unit import UnitMetadata
from misc.unit_creator import UNIT_UI
from ndf_parse.model import List, ListRow
from utils.ndf import to_List as qlist

def create(ctx: UnitCreationContext) -> UnitInfo | None:
    # ✪ M998 HUMVEE SGT.
    with ctx.create_unit("M998 HUMVEE SGT.", "US", "M1025_Humvee_CMD_US") as m998_humvee_sgt:
        # add tiny amount of cargo capacity
        # update cost, AI stuff to compensate
        return UnitInfo(m998_humvee_sgt, 2, [0, 4, 3, 0])
        