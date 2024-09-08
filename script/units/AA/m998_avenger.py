from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.deck_unit_info import TDeckUniteRule
from misc.unit_creator import UNIT_UI
from ndf_parse.model import List

def create(ctx: UnitCreationContext) -> tuple[tuple[str, int], TDeckUniteRule]:
    # M998 AVENGER
    # copy AB M998 AVENGER
    with ctx.create_unit("M998_Avenger_US", "M998_Avenger_US") as m998_avenger:
        # remove forward deploy
        m998_avenger.remove_module("TDeploymentShiftModuleDescriptor")
        # remove para trait
        m998_avenger.edit_ui_module(SpecialtiesList=['AA'])
        rule = TDeckUniteRule(
            m998_avenger.new.descriptor_path,
            AvailableWithoutTransport=True,
            # TODO: automatically get this from AB M998 AVENGER
            NumberOfUnitInPack=4,
            # unit rule xp should also be higher
            NumberOfUnitInPackXpMultiplier=[0, 1, 0.6, 0]
        )
        return ((m998_avenger.new.deck_pack_descriptor_path, 2), rule)
        