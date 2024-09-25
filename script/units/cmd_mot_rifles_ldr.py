from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
from units._utils import edit_standard_squad


def create(ctx: ModCreationContext) -> UnitRules | None:
    # CMD MOT. RIFLES LDR.
    with ctx.create_unit("#CMD MOT. RIFLES LDR.", "US", "LightRifles_CMD_US") as mot_rifles_ldr:
        # change squad count from 6 to 8
        edit_standard_squad(mot_rifles_ldr, 6, 2, 26, 92)
        #   change in models - make custom Gfx thing with custom AllWeaponsSubdepiction_xx_US
        #       or maybe i can just steal it from a unit with the appropriate weapons? i.e. FIRE TEAM (AT-4)
        with mot_rifles_ldr.module_context('ApparenceModel', by_name=True) as apparence_module:
            apparence_module.edit_members(Depiction='~/Gfx_Rifles_half_AT4_US')
        # make custom showroom unit
        return UnitRules(mot_rifles_ldr, 2, [0, 6, 4, 0])
        