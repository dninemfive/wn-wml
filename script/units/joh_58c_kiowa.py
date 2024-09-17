from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from metadata.division_unit_registry import UnitInfo
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow
from utils.ndf.misc import to_List as qlist


def create(ctx: ModCreationContext) -> UnitInfo | None:
    # JOH-58C Kiowa
    # Copy of: OH-58C/S
    with ctx.create_unit("JOH-58C KIOWA", "US", "OH58_CS_US") as joh_58c_kiowa:
        # reduce stinger count
        # add minigun
        # adjust missile carriage?
        return UnitInfo(joh_58c_kiowa, 2, [0, 4, 3, 0])
        