from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
import utils.ndf.unit_module as module
from units._utils import edit_standard_squad
from units._weapons import M16A2, M249, TOW_SCAT
from model.squads.squad import Squad


def create(ctx: ModCreationContext) -> UnitRules | None:
    # SCAT
    with ctx.create_unit("#RECO2 SCAT", "US", "Scout_US") as scat:
        squad: Squad = Squad.copy_parent(ctx.guids, scat, 'US', (M16A2, 5), (M249, 1), (TOW_SCAT, 1))
        squad.apply(ctx.ndf, scat.msg)
        squad.edit_unit(scat)
        scat.UpgradeFromUnit='d9_RECO2_FOLT_US'
        return UnitRules(scat, 3, [0, 6, 4, 0])