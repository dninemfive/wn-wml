from context.mod_creation import ModCreationContext
from context.unit_module import UnitModuleContext
from creators.unit.basic import UNIT_UI
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow
import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
import utils.ndf.unit_module as module


def create(ctx: ModCreationContext) -> UnitRules | None:
    # XM119 IMCS
    # copy VLRA mortar
    with ctx.create_unit("XM1100 120mm", "US", "VLRA_Mortier81_FR") as xm1100_120mm:
        xm1100_120mm.edit_ui_module(SpecialtiesList=["'mortar'"],
                                  UpgradeFromUnit='Descriptor_Unit_Mortier_107mm_US')
        # change main weapon to a somewhat improved version of the M30 (or maybe the Tampella?)
        # change country (+flag) to US
        xm1100_120mm.MotherCountry = 'US'
        xm1100_120mm.remove_module('TDeploymentShiftModuleDescriptor')
        return UnitRules(xm1100_120mm, 2, [0, 4, 3, 0])
        