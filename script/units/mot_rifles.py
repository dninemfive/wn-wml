from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
from units._weapons import M16A2, M249, AT4
from model.squads.squad import InfantryUnitCreator

def create(ctx: ModCreationContext) -> UnitRules | None:
    # MOT. RIFLES.
    with ctx.create_unit("MOT. RIFLES", "US", "Rifles_half_AT4_US") as mot_rifles:
        squad: InfantryUnitCreator = InfantryUnitCreator.copy_parent(ctx.guids, mot_rifles, 'US', (M16A2, 7), (M249, 2), (AT4, 1))
        squad.apply(ctx.ndf, mot_rifles.msg)
        squad.edit_unit(mot_rifles)
        mot_rifles.UpgradeFromUnit='d9_CMD_MOT_RIFLES_LDR_US'
        mot_rifles.CommandPointCost = 55
        return UnitRules(mot_rifles, 2, [0, 6, 4, 0])