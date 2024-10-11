import utils.ndf.edit as edit
import utils.ndf.unit_module as module
from units._weapons import M16A2, M249
from context.mod_creation import ModCreationContext
from metadata.division_unit_registry import UnitRules


def create(ctx: ModCreationContext) -> UnitRules | None:
    # MOT. SCOUTS
    with ctx.create_infantry_unit("#RECO2 MOT. SCOUTS", "US", "Scout_US", [(M16A2, 3), (M249, 1)]) as mot_scouts:
        # insert between scouts and ab scouts
        mot_scouts.modules.ui.UpgradeFromUnit='Scout_US'
        ctx.get_unit('Airborne_Scout_US').modules.ui.UpgradeFromUnit = mot_scouts
        # TODO: have it automatically copy availability from parent if not specified
        return UnitRules(mot_scouts, 3, [0, 6, 4, 0])