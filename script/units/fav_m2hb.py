import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
import utils.ndf.unit_module as module
from constants import ndf_paths
from context.mod_creation import ModCreationContext
from context.unit_module import UnitModuleContext
from creators.unit.basic import UNIT_UI
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow, MemberRow, Object


def create(ctx: ModCreationContext) -> UnitRules | None:
    # 👓 FAV AGL
    # model: ILTIS HMG
    # range: custom
    # air transportable
    with ctx.create_unit("#RECO1 FAV M2HB", "US", "Iltis_HMG_BEL") as fav:
        fav.modules.type.edit_members(
            MotherCountry='US'                             # TODO: set this, icon flag, &c with one item
        )
        fav.command_point_cost = 45
        fav.modules.ui.edit_members(
            SpecialtiesList=['reco', 'air_transportable']
        )
        fav.modules.remove('Transporter', by_name=True)
        return UnitRules(fav, 2, [0, 4, 3, 0], 'UH60A_Black_Hawk_US', True)