
from context.mod_creation import ModCreationContext
from context.unit_module import UnitModuleContext
from creators.unit.basic import UNIT_UI
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
        m966_humvee_tow.modules.ui.UpgradeFromUnit='M274_Mule_ITOW_US'
        # insert before M1025 Humvee TOW
        ctx.get_unit('M1025_Humvee_TOW_US').modules.ui.UpgradeFromUnit = m966_humvee_tow
        return UnitRules(m966_humvee_tow, 3, [0, 4, 3, 0])
