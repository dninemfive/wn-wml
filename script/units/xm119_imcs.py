from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
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
        xm119_imcs.remove_tags('Artillerie_Courte_Portee')
        xm119_imcs.add_tags('Artillerie_Longue_Portee')
        with xm119_imcs.module_context('TTacticalLabelModuleDescriptor') as tactical_label_module:
            edit.members(tactical_label_module.object.by_member('IdentifiedTexture').value, Values=['"Texture_RTS_H_howitzer"', '"Texture_howitzer"'])
        xm119_imcs.edit_ui_module(SpecialtiesList=["'howitzer'"],
                                  TypeStrategicCount='ETypeStrategicDetailedCount/Howitzer',
                                  UnitRole="'tank_C'",
                                  UpgradeFromUnit='Descriptor_Unit_Howz_M102_105mm_US')
        # change main weapon to a somewhat improved version of the M102 (a bit better fire rate + RAP projectiles, probably)
        m198 = xm119_imcs.get_other_unit('Howz_M198_155mm_US')
        edit.members(module.get(m198, 'TUnitUIModuleDescriptor'), UpgradeFromUnit=None)
        # change country (+flag) to US
        xm119_imcs.MotherCountry = 'US'
        xm119_imcs.remove_module('TDeploymentShiftModuleDescriptor')
        return UnitRules(xm119_imcs, 2, [0, 4, 3, 0])
        