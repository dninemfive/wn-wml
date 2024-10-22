import mw2.utils.ndf.edit as edit
from mw2.context.mod_creation import ModCreationContext
from mw2.context.unit_module import UnitModuleContext
from mw2.creators.ammo import AmmoCreator
from mw2.creators.unit.basic import UNIT_UI
from mw2.creators.weapon import WeaponCreator
from mw2.metadata.unit import UnitMetadata
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair
from ndf_parse.model import List, ListRow


def create(ctx: ModCreationContext) -> NewSrcUnitPair | None:
    with ctx.create_unit("XM142 HIMARS [ATACMS]", "US", "BM21_Grad_SOV") as xm142_himars_atacms:
        # TODO: weapon
        # update speed, fuel capacity
        xm142_himars_atacms.unit.set_country('US')
        # change unit dangerousness
        # change unit attack/defense value
        # change unit cost
        xm142_himars_atacms.modules.ui.UpgradeFromUnit = 'd9_XM142_HIMARS_CLU_US'
        return xm142_himars_atacms
        