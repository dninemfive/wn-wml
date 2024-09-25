
from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow, Object
import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
from constants.ndf_paths import WEAPON_DESCRIPTOR


def create(ctx: ModCreationContext) -> UnitRules | None:
    # M966 HUMVEE TOW
    with ctx.create_unit("M966 HUMVEE TOW", "US", "M1025_Humvee_TOW_US") as m966_humvee_tow:
        with m966_humvee_tow.edit_weapons('M1025_Humvee_TOW_US') as weapons:
            weapons.edit_members(Salves=[6,])
        m966_humvee_tow.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_M274_Mule_ITOW_US')
        # insert before M1025 Humvee TOW
        with ModuleContext(m966_humvee_tow.get_other_unit('M1025_Humvee_TOW_US'), 'TUnitUIModuleDescriptor') as m1025_ui_module:
            m1025_ui_module.edit_members(UpgradeFromUnit='Descriptor_Unit_d9_M966_HUMVEE_TOW_US')
        return UnitRules(m966_humvee_tow, 3, [0, 4, 3, 0])
