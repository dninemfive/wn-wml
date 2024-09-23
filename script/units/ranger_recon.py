from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI, UnitCreator
from metadata.division_unit_registry import UnitRules
from ndf_parse.model import List
import utils.ndf.edit as edit
from units._utils import edit_standard_squad


def create(ctx: ModCreationContext) -> UnitRules | None:
    # RANGER RECON
    with ctx.create_unit("#RECO2 RANGER RECON", "US", "LRRP_US") as ranger_recon:
        # weapons: 
        # - M16A2 x3
        # - M60E3 x1    (new ammo using M60 model but better accuracy while moving and usable indoors)
        # - M21   x1
        # - M203  x1    (new ammo, needs custom texture and balancing; basically a long-range but much weaker version of demo charges)
        # - smoke?
        # make custom showroom unit
        # insert after AB scouts
        ranger_recon.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_Airborne_Scout_US')
        # TODO: update appearance to have weapons match
        return UnitRules(ranger_recon, 1, [0, 0, 4, 2])