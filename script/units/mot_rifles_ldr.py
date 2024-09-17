from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from model.deck_unite_rule import TDeckUniteRule
from ndf_parse.model import List

def create(ctx: ModCreationContext) -> tuple[tuple[str, int], TDeckUniteRule]:
    # ✪ MOT. RIFLES LDR.
    # see: FM 71-2 appendix A fig. A-11 CO HQ
    # copy: Airborne Ldr.
    with ctx.create_unit("MOT. RIFLES LDR.", "US", "Airborne_CMD_US") as mot_rifles_ldr:
        # 6x M16A2, 2x M240B
        # remove Shock and Airborne traits
        # remove forward deploy
        # reduce cost
        # change TTypeUnitModuleDescriptor:TypeUnitFormation from Supply?

        rule = TDeckUniteRule(
            mot_rifles_ldr.new.descriptor_path,
            AvailableWithoutTransport=False,
            # TODO: decide on transports
            AvailableTransportList=["$/GFX/Unit/Descriptor_Unit_M998_Humvee_US"],
            # TODO: automatically get this from Airborne CMD
            NumberOfUnitInPack=6,
            # unit rule xp should also be higher
            NumberOfUnitInPackXPMultiplier=[0, 1, 0.6, 0]
        )
        return ((mot_rifles_ldr.new.deck_pack_descriptor_path, 2), rule)
        