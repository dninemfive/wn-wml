import mw2.constants.ndf_paths as ndf_paths
from mw2.context.mod_creation import ModCreationContext
from mw2.context.unit_module import UnitModuleContext
from mw2.creators.unit.abc import UnitCreator
from mw2.creators.unit.basic import BasicUnitCreator
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair
from mw2.utils.ndf import ensure
from ndf_parse.model import List, ListRow, MemberRow, Object


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # ✪ M997 TC3V
    # TODO: add a little icon after/instead of the cmd one indicating that it has a larger command radius
    # TODO: larger command radius than usual
    with ctx.create_unit("#CMD M997 TC3V", "US", "M1025_Humvee_CMD_US", 'M1038_Humvee_US') as m997_tc3v:
        m997_tc3v.modules.replace_from_many(
            'M1038_Humvee_US',
            ('ApparenceModel', True),
            'TCadavreGeneratorModuleDescriptor',
            'TBaseDamageModuleDescriptor'
        )
        m997_tc3v.modules.production.command_point_cost = 95
        m997_tc3v.modules.ui.ButtonTexture = 'M1038_Humvee_US'
        m997_tc3v.modules.ui.UpgradeFromUnit = 'M1025_Humvee_CMD_US'
        return m997_tc3v