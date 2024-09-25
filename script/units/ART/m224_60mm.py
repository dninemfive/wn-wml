from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
from units._utils import edit_standard_squad


def create(ctx: ModCreationContext) -> UnitRules | None:
    # M224 60mm
    with ctx.create_unit("M224 60mm", "US", "Rifles_HMG_US") as rangers_m203:
        # change squad count to 10
        # weapons:
        # - M16A2 x6
        # - M224 60mm x2
        # create M224 60mm def
        # edit WeaponDescriptor:
        #   replace slot 0 with M16A2
        #   replace slot 1 with M224 60mm
        # make custom showroom unit
        rangers_m203.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_d9_Mk19_40mm_US')
        return UnitRules(rangers_m203, 2, [0, 6, 4, 0])