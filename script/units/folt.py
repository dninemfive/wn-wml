from script.context.mod_creation import ModCreationContext
from script.context.unit_module import UnitModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
import utils.ndf.unit_module as module
from units._utils import edit_standard_squad
from units._weapons import M16A2
from script.creators.unit.infantry import InfantryUnitCreator


def create(ctx: ModCreationContext) -> UnitRules | None:
    # FOLT
    with ctx.create_unit("#RECO2 FOLT", "US", "Scout_US") as folt:
        squad: InfantryUnitCreator = InfantryUnitCreator.copy_parent(ctx.guids, folt, 'US', (M16A2, 2))
        squad.apply(ctx.ndf, folt.msg)
        squad.edit_unit(folt)
        # TODO: GSR trait
        return UnitRules(folt, 3, [0, 6, 4, 0])