from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair
from ..infantry_weapons import M16A2, M249
from mw2.context.mod_creation import ModCreationContext


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # MOT. SCOUTS
    with ctx.create_infantry_unit("#RECO2 MOT. SCOUTS", "US", "Scout_US", [(M16A2, 3), (M249, 1)]) as mot_scouts:
        # insert between scouts and ab scouts
        mot_scouts.modules.ui.UpgradeFromUnit='Scout_US'
        ctx.get_unit('Airborne_Scout_US').modules.ui.UpgradeFromUnit = mot_scouts
        # TODO: have it automatically copy availability from parent if not specified
        return mot_scouts