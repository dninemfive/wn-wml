
from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair
from ndf_parse.model import List, ListRow, Object


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    with ctx.create_unit("XM4 SLAMMER", "US", "Marder_1A3_RFA") as xm4_slammer:
        # TODO: set weapons and armor appropriately
        xm4_slammer.modules.ui.UpgradeFromUnit=None
        return xm4_slammer