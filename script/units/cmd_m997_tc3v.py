import constants.ndf_paths as ndf_paths
from context.mod_creation import ModCreationContext
from context.unit_module import UnitModuleContext
from creators.unit.basic import BasicUnitCreator
from metadata.unit_rules import UnitRules
from ndf_parse.model import List, ListRow, MemberRow, Object
from utils.ndf import ensure
from units._utils import autonomy_to_fuel_move_duration as to_fmd


def create(ctx: ModCreationContext) -> UnitRules | None:
    # ✪ M997 TC3V
    # TODO: add a little icon after/instead of the cmd one indicating that it has a larger command radius
    # TODO: larger command radius than usual
    with ctx.create_unit("#CMD M997 TC3V", "US", "M1025_Humvee_CMD_US", 'M1038_Humvee_US') as m997_tc3v: # 🏳️‍⚧️
        m997_tc3v.modules.replace_from_many(
            'M1038_Humvee_US',
            ('ApparenceModel', True),
            'TCadavreGeneratorModuleDescriptor',
            'TBaseDamageModuleDescriptor'
        )
        m997_tc3v.modules.production.command_point_cost = 95
        m997_tc3v.modules.ui.ButtonTexture = 'M1038_Humvee_US'
        m997_tc3v.modules.ui.UpgradeFromUnit = 'M1025_Humvee_CMD_US'
        return UnitRules(m997_tc3v, 1, [0, 3, 2, 0])