from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.deck_unit_info import TDeckUniteRule

def create(ctx: UnitCreationContext) -> tuple[tuple[str, int], TDeckUniteRule] | None:
    # M998 HUMVEE AGL
    with ctx.create_unit("M998 HUMVEE M2HB", "US", "M1025_Humvee_scout_US") as m998_humvee_agl:
        # upgrade from M998 HUMVEE SQC
        m998_humvee_agl.edit_ui_module(UpgradeFromUnit="Descriptor_Unit_M998_HUMVEE_SQC_US")
        # bad vision
        # specialties = transport, _transport1
        # MenuIconTexture = (not recon)
        # TTacticalLabelModuleDescriptor: identified texture is transport, not reco
        # transports don't get added to divisions separately
        return None