from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.deck_unit_info import TDeckUniteRule

def create(ctx: UnitCreationContext) -> tuple[tuple[str, int], TDeckUniteRule]:
    # M1075 PLS
    # copy of: HEMTT
    with ctx.create_unit("M1075 PLS SUPPLY", "US", "HEMTT_US") as m1075_pls:
        m1075_pls.edit_ui_module(UpgradeFromUnit="Descriptor_Unit_d9_M998_HUMVEE_SUPPLY_US")
        rule = TDeckUniteRule(
            m1075_pls.new.descriptor_path,
            AvailableWithoutTransport=True,
            AvailableTransportList=None,
            # TODO: automatically get this from HEMTT
            NumberOfUnitInPack=3,
            # unit rule xp should also be higher
            NumberOfUnitInPackXpMultiplier=[0, 1, 0.68, 0]
        )
        return ((m1075_pls.new.deck_pack_descriptor_path, 1), rule)