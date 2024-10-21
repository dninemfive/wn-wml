from context.mod_creation import ModCreationContext
from context.unit_module import UnitModuleContext
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
import utils.ndf.unit_module as module
from units._weapons import M16A2
from creators.unit.infantry import InfantryUnitCreator


def create(ctx: ModCreationContext) -> UnitRules | None:
    # FOLT
    with ctx.create_infantry_unit("#RECO2 FOLT", "US", "Scout_US", [(M16A2, 2)]) as folt:
        # TODO: GSR trait
        return UnitRules(folt, 3, [0, 6, 4, 0])