from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.deck_unit_info import TDeckUniteRule

def create(ctx: UnitCreationContext) -> tuple[tuple[str, int], TDeckUniteRule] | None:
    # M998 HUMVEE AGL
    # copy the recon version, but normal vision (actually Bad bc all transports seem to have that)
    with ctx.create_unit("M998 HUMVEE AGL", "US", "M1025_Humvee_AGL_nonPara_US") as m998_humvee_agl:
        # upgrade from M998 HUMVEE SQC
        m998_humvee_agl.edit_ui_module(UpgradeFromUnit="Descriptor_Unit_M998_HUMVEE_M2HB_US")
        # bad vision
        # specialties = transport, _transport1
        # MenuIconTexture = (not recon)
        # TTacticalLabelModuleDescriptor: identified texture is transport, not reco
        # transports don't get added to divisions separately
        return None