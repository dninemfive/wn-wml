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
    with ctx.create_unit("XM119 IMCS 105mm", "US", "VLRA_Mortier81_FR") as xm119_imcs:
        # add tag Artillerie_Longue_Portee
        xm119_imcs.tags.remove('Artillerie_Courte_Portee')
        xm119_imcs.tags.add('Artillerie_Longue_Portee')
        edit.members(xm119_imcs.modules.get('TTacticalLabelModuleDescriptor').by_member('IdentifiedTexture').value,
                        Values=['"Texture_RTS_H_howitzer"', '"Texture_howitzer"'])
        xm119_imcs.modules.ui.edit_members(SpecialtiesList=['howitzer'],
                                           TypeStrategicCount='Howitzer',
                                           UnitRole='tank_C',
                                           UpgradeFromUnit='Howz_M102_105mm_US')
        # change main weapon to a somewhat improved version of the M102 (a bit better fire rate + RAP projectiles, probably)
        ctx.get_unit('Howz_M198_155mm_US').modules.ui.UpgradeFromUnit = None
        # change country (+flag) to US
        xm119_imcs.modules.type.MotherCountry = 'US'
        xm119_imcs.modules.remove('TDeploymentShiftModuleDescriptor')
        return UnitRules(xm119_imcs, 2, [0, 4, 3, 0])
        