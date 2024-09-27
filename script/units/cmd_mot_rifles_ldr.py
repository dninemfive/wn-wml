from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
from units._utils import edit_standard_squad
from units._weapons import M16A2, M240
from model.squads.squad import Squad


def create(ctx: ModCreationContext) -> UnitRules | None:
    # CMD MOT. RIFLES LDR.
    with ctx.create_unit("#CMD MOT. RIFLES LDR.", "US", "Rifles_CMD_US") as mot_rifles_ldr:
        squad: Squad = Squad.copy_parent(ctx.guids, mot_rifles_ldr, 'US', (M16A2, 5), (M240, 1))
        squad.apply(ctx.ndf, mot_rifles_ldr.msg)
        squad.edit_unit(mot_rifles_ldr)
        return UnitRules(mot_rifles_ldr, 2, [0, 6, 4, 0])
        