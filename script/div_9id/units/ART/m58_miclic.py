from mw2.context.mod_creation import ModCreationContext
from mw2.context.unit_module import UnitModuleContext
from mw2.metadata.unit import UnitMetadata
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair
import mw2.utils.ndf.ensure as ensure
import mw2.utils.ndf.edit as edit


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    with ctx.create_unit("M58 MICLIC", "US", "Mortier_2B9_Vasilek_SOV") as m58_miclic:
        # set ammo to Ammo_RocketArt_PW_MICLICS
        m58_miclic.modules.ui.UpgradeFromUnit=None
        m58_miclic.unit.set_country('US')
        return m58_miclic