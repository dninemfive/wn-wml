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
    # FWD SUPPORT [EW]
    with ctx.create_unit("#RECO1 FWD SUPPORT [EW]", "US", "Scout_US") as fwd_support:
        # TODO: change weapon loadout
        squad: Squad = Squad.copy_parent(ctx.guids, fwd_support, 'US', (M16A2, 4), (M249, 1), (AT4, 1))
        squad.apply(ctx.ndf, fwd_support.msg)
        squad.edit_unit(fwd_support)
        # TODO: reduce vision
        # TODO: add traits: EW, GSR, direction finding?
        fwd_support.UpgradeFromUnit='d9_RECO1_OPERATIONAL_SUPPORT_US'
        return UnitRules(fwd_support, 3, [0, 6, 4, 0])