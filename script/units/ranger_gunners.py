from script.context.mod_creation import ModCreationContext
from script.context.unit_module import UnitModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
from units._utils import edit_standard_squad
from units._weapons import M16A2, M60E3
from script.creators.unit.infantry import InfantryUnitCreator

def create(ctx: ModCreationContext) -> UnitRules | None:
    # RANGER GUNNERS
    with ctx.create_unit("RANGER GUNNERS", "US", "Ranger_US") as ranger_gunners:
        squad: InfantryUnitCreator = InfantryUnitCreator.copy_parent(ctx.guids, ranger_gunners, 'US', (M16A2, 7), (M60E3, 1), (M60E3, 1), (M60E3, 1))
        squad.apply(ctx.ndf, ranger_gunners.msg)
        squad.edit_unit(ranger_gunners)
        ranger_gunners.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_Airborne_HMG_US')
        return UnitRules(ranger_gunners, 2, [0, 6, 4, 0])