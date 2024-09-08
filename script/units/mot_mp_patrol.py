from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.deck_unit_info import TDeckUniteRule
from misc.unit_creator import UNIT_UI
from ndf_parse.model import List

def create(ctx: UnitCreationContext) -> tuple[tuple[str, int], TDeckUniteRule]:
    # MOT. MP PATROL
    # (just copy AB MP PATROL)
    with ctx.create_unit("MOT. MP PATROL", "US", "Airborne_MP_US") as mp_patrol:
        with mp_patrol.module_context(UNIT_UI) as ui_module:
            specialties: List = ui_module.object.by_member("SpecialtiesList").value
            specialties.remove(specialties.find_by_cond(lambda x: x == "_para"))
            ui_module.edit_members(SpecialtiesList=specialties)
        mp_patrol.remove_module("TDeploymentShiftModuleDescriptor")
        rule = TDeckUniteRule(
            mp_patrol.new.descriptor_path,
            AvailableWithoutTransport=False,
            # TODO: decide on transports. maybe include MP Humvee?
            AvailableTransportList=["$/GFX/Unit/Descriptor_Unit_M998_Humvee_US"],
            # TODO: automatically get this from HEMTT
            NumberOfUnitInPack=6,
            # unit rule xp should also be higher
            NumberOfUnitInPackXpMultiplier=[0, 1, 0.6, 0]
        )
        return ((mp_patrol.new.deck_pack_descriptor_path, 2), rule)
        