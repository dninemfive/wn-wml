from dataclasses import dataclass
from metadata.division import DivisionMetadata
from metadata.unit import UnitMetadata
from misc.unit_creator import UnitCreator
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from typing import Self
from utils.ndf import map_from_rows, make_obj, to_List

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
        self.rule = TDeckUniteRule.make(unit, units_per_pack, transports, force_awt)

    @property
    def pack(self: Self) -> MapRow:
        return MapRow(key=self.unit.deck_pack_descriptor_path, value=self.num_packs)

    @staticmethod
    def from_vanilla(unit: UnitMetadata, num_packs: int, *divisions_for_rule: str) -> Self:
        pass

@dataclass
class TDeckUniteRule(object):
    UnitDescriptor: str
    AvailableWithoutTransport: bool
    AvailableTransportList: list[str] | None
    NumberOfUnitInPack: int
    NumberOfUnitInPackXPMultiplier: tuple[float, float, float, float]

    def to_obj(self: Self) -> Object:
        result = Object('TDeckUniteRule')
        result.add(MemberRow(self.UnitDescriptor, "UnitDescriptor"))
        result.add(MemberRow(str(self.AvailableWithoutTransport), "AvailableWithoutTransport"))
        if(self.AvailableTransportList is not None):
            result.add(MemberRow(to_List(*self.AvailableTransportList), "AvailableTransportList"))
        result.add(MemberRow(str(self.NumberOfUnitInPack), "NumberOfUnitInPack"))
        result.add(MemberRow(to_List(*[str(x) for x in self.NumberOfUnitInPackXPMultiplier]), "NumberOfUnitInPackXPMultiplier"))
        return result
    
    @staticmethod
    def make(metadata: UnitMetadata | UnitCreator,
                   num_per_xp: tuple[int, int, int, int],
                   transports: list[str] | None = None,
                   force_awt: bool | None = None) -> Self:
        if isinstance(metadata, UnitCreator):
            metadata = metadata.new
        num_per_pack = max(num_per_xp)
        xp_multipliers = [x / num_per_pack for x in num_per_xp]
        available_without_transport = force_awt if force_awt is not None else (transports is None)
        return TDeckUniteRule(
            metadata.descriptor_path,
            available_without_transport,
            transports,
            num_per_pack,
            xp_multipliers
        )
    
class DivisionUnits(object):

    def __init__(self: Self, division: DivisionMetadata, *units: UnitInfo):
        self.division = division
        self.units = units

    def register(self: Self, info: UnitInfo):
        self.units.append(info)

    def pack_list(self: Self) -> Map:
        return map_from_rows(x.pack for x in self.units)
    
    def division_rules(self: Self) -> Object:
        return make_obj('TDeckDivisionRule',
                        UnitRuleList=to_List(unit.rule.to_obj()
                                             for unit
                                             in self.units))