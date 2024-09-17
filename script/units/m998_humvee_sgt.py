from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow
from utils.ndf import to_List as qlist


def create(ctx: ModCreationContext) -> UnitRules | None:
    # ✪ M998 HUMVEE SGT.
    with ctx.create_unit("M998 HUMVEE SGT.", "US", "M1025_Humvee_CMD_US") as m998_humvee_sgt:
        # add tiny amount of cargo capacity
        # update cost, AI stuff to compensate
        return UnitRules(m998_humvee_sgt, 2, [0, 4, 3, 0])
        