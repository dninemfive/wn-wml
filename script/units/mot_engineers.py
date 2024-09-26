import utils.ndf.edit as edit
import utils.ndf.unit_module as module
from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
from units._utils import edit_standard_squad
from _weapons import M16A2, M249, SATCHEL_CHARGE
from model.squads.squad import Squad


def create(ctx: ModCreationContext) -> UnitRules | None:
    # MOT. RIFLES.
    with ctx.create_unit("MOT. ENGINEERS", "US", "Engineers_US") as mot_engineers:
        squad: Squad = Squad.copy_parent(ctx.guids, mot_engineers, 'US', (M16A2, 7), (M249, 1))
        squad.apply(ctx.ndf, mot_engineers.msg)
        squad.edit_unit(mot_engineers)
        # insert between engineers and engineers (FLASH)
        mot_engineers.UpgradeFromUnit = 'Engineers_US'
        engineers_flash = mot_engineers.get_other_unit('Engineers_Flash_US')
        edit.members(module.get(engineers_flash, 'TUnitUIModuleDescriptor'), UpgradeFromUnit='Descriptor_Unit_d9_MOT_ENGINEERS_US')
        return UnitRules(mot_engineers, 2, [0, 6, 4, 0])