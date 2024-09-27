from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
import utils.ndf.unit_module as module
from units._utils import edit_standard_squad
from units._weapons import M16A2, M249, AT4
from model.squads.squad import Squad


def create(ctx: ModCreationContext) -> UnitRules | None:
    # OPERATIONAL SUPPORT
    with ctx.create_unit("#RECO1 OPERATIONAL SUPPORT", "US", "Scout_US") as op_support:
        # TODO: change weapon loadout
        squad: Squad = Squad.copy_parent(ctx.guids, op_support, 'US', (M16A2, 8), (M249, 4), (AT4, 2))
        squad.apply(ctx.ndf, op_support.msg)
        squad.edit_unit(op_support)
        # TODO: increase menace
        # TODO: reduce vision
        # op_support.UpgradeFromUnit=None
        return UnitRules(op_support, 3, [0, 6, 4, 0])