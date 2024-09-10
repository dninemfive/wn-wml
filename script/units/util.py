from metadata.deck_unit_info import TDeckUniteRule
from metadata.unit import UnitMetadata
from misc.unit_creator import UnitCreator

def make_unit_rule(metadata: UnitMetadata | UnitCreator,
                   num_per_xp: tuple[int, int, int, int],
                   num_packs: int,
                   transports: list[str] | None = None,
                   force_awt: bool | None = None) -> tuple[tuple[str, int], TDeckUniteRule]:
    if isinstance(metadata, UnitCreator):
        metadata = metadata.new
    num_per_pack = max(num_per_xp)
    xp_multipliers = [x / num_per_pack for x in num_per_xp]
    available_without_transport = force_awt if force_awt is not None else (transports is None)
    rule = TDeckUniteRule(
        metadata.descriptor_path,
        available_without_transport,
        transports,
        num_per_pack,
        xp_multipliers
    )
    return ((metadata.deck_pack_descriptor_path, num_packs), rule)