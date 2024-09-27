from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
from units._utils import edit_standard_squad
from units._weapons import M16A2
from model.squads.squad import Squad

def create(ctx: ModCreationContext) -> UnitRules | None:
    # RANGER AT SECTION
    with ctx.create_unit("RANGER AT SECTION", "US", "Ranger_US") as rangers_m67:
        # change squad count to 10
        # weapons:
        # - M16A2 x10
        # - M67 90mm
        # - M67 90mm
        # - M67 90mm
        squad: Squad = Squad.copy_parent(ctx.guids, rangers_m67, 'US', (M16A2, 10))
        squad.apply(ctx.ndf, rangers_m67.msg)
        squad.edit_unit(rangers_m67)
        rangers_m67.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_d9_RANGERS_M203_US')
        return UnitRules(rangers_m67, 2, [0, 6, 4, 0])