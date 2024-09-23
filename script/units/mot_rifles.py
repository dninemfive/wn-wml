from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
from units._utils import edit_standard_squad


def create(ctx: ModCreationContext) -> UnitRules | None:
    # MOT. RIFLES.
    with ctx.create_unit("MOT. RIFLES", "US", "Rifles_half_AT4_US") as mot_rifles:
        # change squad count from 6 to 9        
        edit_standard_squad(mot_rifles, 7, 2, 26, 92)
        # make custom showroom unit
        mot_rifles.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_d9_CMD_MOT_RIFLES_LDR_US')
        return UnitRules(mot_rifles, 2, [0, 6, 4, 0])