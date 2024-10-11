from context.mod_creation import ModCreationContext
from context.unit_module import UnitModuleContext
from creators.unit.basic import UNIT_UI
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow
import utils.ndf.ensure as ensure


def create(ctx: ModCreationContext) -> UnitRules | None:
    # M998 AVENGER
    # copy AB M998 AVENGER
    with ctx.create_unit("M998 Avenger", "US", "M998_Avenger_US") as m998_avenger:
        # remove forward deploy
        m998_avenger.modules.remove("TDeploymentShiftModuleDescriptor")
        # remove para trait
        m998_avenger.modules.ui.SpecialtiesList.remove('_para')
        # make AB M998 AVENGER upgrade from M998 AVENGER
        ctx.get_unit('M998_Avenger_US').modules.ui.UpgradeFromUnit = m998_avenger
        # TODO: maybe allow deployment via CH-47D?
        return UnitRules(m998_avenger, 2, [0, 4, 3, 0])
        