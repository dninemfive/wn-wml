import utils.ndf.edit as edit
import utils.ndf.unit_module as module
from _weapons import M16A2, M249
from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from model.squads.squad import Squad
from ndf_parse.model import List
from units._utils import edit_standard_squad


def create(ctx: ModCreationContext) -> UnitRules | None:
    # MOT. SCOUTS
    with ctx.create_unit("#RECO2 MOT. SCOUTS", "US", "Scout_US") as mot_scouts:
        squad: Squad = Squad.copy_parent(ctx.guids, mot_scouts, 'US', (M16A2, 3), (M249, 1))
        squad.apply(ctx.ndf, mot_scouts.msg)
        squad.edit_unit(mot_scouts)
        # insert between scouts and ab scouts
        mot_scouts.UpgradeFromUnit='Unit_Scout_US'
        ab_scouts = mot_scouts.get_other_unit('Descriptor_Unit_Airborne_Scout_US')
        edit.members(module.get(ab_scouts, 'TUnitUIModuleDescriptor'), UpgradeFromUnit='Descriptor_Unit_d9_RECO2_MOT_SCOUTS_US')
        # TODO: have it automatically copy availability from parent if not specified
        return UnitRules(mot_scouts, 3, [0, 6, 4, 0])