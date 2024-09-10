from dataclasses import dataclass
from metadata.division import DivisionMetadata
from metadata.unit import UnitMetadata
from misc.unit_creator import UnitCreator
from ndf_parse.model import List, ListRow, MemberRow, Object
from typing import Self
from utils.ndf import make_obj, to_List

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
    division: DivisionMetadata
    units: list[UnitInfo]

    def __init__(self: Self, division: DivisionMetadata):
        self.division = division

    def register(self: Self, info: UnitInfo):
        self.units.append(info)

    def DivisionRules(self: Self) -> tuple[str, Object]:
        unit_rule_list = List()
        for unit in self.units:
            unit_rule_list.add(ListRow(unit.rule.to_obj()))
        return (self.division.descriptor_path, make_obj('TDeckDivisionRule', UnitRuleList=unit_rule_list))