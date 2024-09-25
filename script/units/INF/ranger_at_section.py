from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
from units._utils import edit_standard_squad


def create(ctx: ModCreationContext) -> UnitRules | None:
    # RANGER AT SECTION
    with ctx.create_unit("RANGER AT SECTION", "US", "Ranger_US") as rangers_m203:
        # change squad count to 10
        # weapons:
        # - M16A2 x10
        # - M67 90mm
        # - M67 90mm
        # - M67 90mm
        # edit WeaponDescriptor:
        #   replace slot 0 with M16A2
        #   replace slot 1 with M67 90mm
        #   replace slot 2 with M67 90mm
        #   append M67 90mm to weapons
        # make custom showroom unit
        rangers_m203.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_d9_RANGERS_M203_US')
        return UnitRules(rangers_m203, 2, [0, 6, 4, 0])