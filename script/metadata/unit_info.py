from dataclasses import dataclass
from message import Message, try_nest
from metadata.division import DivisionMetadata
from metadata.unit import UnitMetadata
from model.deck_unite_rule import TDeckUniteRule
from misc.unit_creator import UnitCreator
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from typing import Self
from utils.ndf.misc import map_from_rows, make_obj, to_List

class UnitInfo(object):
    def __init__(self: Self,
                 unit: UnitMetadata | UnitCreator,
                 num_packs: int,
                 units_per_pack: tuple[int, int, int, int],
                 transports: list[str] | None = None,
                 force_awt: bool | None = None):
        if isinstance(unit, UnitCreator):
            unit = unit.new
        self.unit: UnitMetadata = unit
        self.num_packs = num_packs
        self.rule: TDeckUniteRule = TDeckUniteRule.make(unit, units_per_pack, transports, force_awt)

    @property
    def pack(self: Self) -> MapRow:
        return MapRow(key=self.unit.deck_pack_descriptor_path, value=str(self.num_packs))

    @staticmethod
    def from_deck_unite_rule(unit: UnitMetadata, num_packs: int, rule: TDeckUniteRule) -> Self:
        base_units_per_pack: int = int(rule.NumberOfUnitInPack)
        return UnitInfo(unit,
                        num_packs,
                        tuple(int(x * base_units_per_pack) for x in rule.NumberOfUnitInPackXPMultiplier),
                        rule.AvailableTransportList,
                        rule.AvailableWithoutTransport)