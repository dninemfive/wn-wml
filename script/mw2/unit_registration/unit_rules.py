from typing import Self

from mw2.creators.unit.abc import UnitCreator
from mw2.metadata.unit import UnitMetadata
from mw2.model.deck_unite_rule import TDeckUniteRule
from ndf_parse.model import MapRow

from ._types import Transport, UnitsPerXp


class UnitRules(object):
    def __init__(self: Self,
                 unit: UnitMetadata | UnitCreator,
                 num_packs: int,
                 units_per_pack: UnitsPerXp,
                 transports: list[Transport] | None = None):
        if isinstance(unit, UnitCreator):
            unit = unit.new_unit
        self.unit: UnitMetadata = unit
        self.num_packs = num_packs
        self.rule: TDeckUniteRule = TDeckUniteRule.make(unit, units_per_pack, transports, None in transports)

    @property
    def pack(self: Self) -> MapRow:
        return MapRow(key=self.unit.deck_pack_descriptor.path, value=str(self.num_packs))

    @staticmethod
    def from_deck_unite_rule(unit: UnitMetadata, num_packs: int, rule: TDeckUniteRule) -> Self:
        return UnitRules(unit,
                        num_packs,
                        rule.units_per_xp,
                        rule.AvailableTransportList,
                        rule.AvailableWithoutTransport)