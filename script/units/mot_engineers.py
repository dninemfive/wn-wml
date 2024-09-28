import utils.ndf.edit as edit
import utils.ndf.unit_module as module
from context.mod_creation import ModCreationContext
from metadata.division_unit_registry import UnitRules
from units._weapons import M16A2, M249, SATCHEL_CHARGE
from creators.unit.infantry import InfantryUnitCreator


def create(ctx: ModCreationContext) -> UnitRules | None:
    # MOT. RIFLES.
    with ctx.create_unit("MOT. ENGINEERS", "US", "Engineers_US", [(M16A2, 7), (M249, 1), (SATCHEL_CHARGE, 1)]) as mot_engineers:
        # insert between engineers and engineers (FLASH)
        mot_engineers.UpgradeFromUnit = 'Engineers_US'
        engineers_flash = mot_engineers.get_other_unit('Engineers_Flash_US')
        edit.members(module.get(engineers_flash, 'TUnitUIModuleDescriptor'), UpgradeFromUnit='Descriptor_Unit_d9_MOT_ENGINEERS_US')
        return UnitRules(mot_engineers, 2, [0, 6, 4, 0])