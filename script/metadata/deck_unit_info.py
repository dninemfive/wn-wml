from dataclasses import dataclass
from metadata.division import DivisionMetadata
from ndf_parse.model import List, MemberRow, Object
from typing import Self

@dataclass
class TDeckUniteRule(object):
    UnitDescriptor: str
    AvailableWithoutTransport: bool
    AvailableTransportList: list[str]
    NumberOfUnitInPack: int
    NumberOfUnitInPackXpMultiplier: tuple[float, float, float, float]

    @staticmethod
    def load_from_ndf(ndf: List) -> Self:
        pass
    
class DivisionUnits(object):
    division: DivisionMetadata
    units: list[tuple[tuple[str, int], TDeckUniteRule]]

    def DivisionRules(self: Self) -> tuple[str, Object]:
        unit_rule_list: list[Object] = []
        for _, unit_rule in self.units:
            obj = Object('TDeckUniteRule')
            obj.add(MemberRow(unit_rule.UnitDescriptor, "UnitDescriptor"))
            obj.add(MemberRow(str(unit_rule.AvailableWithoutTransport), "AvailableWithoutTransport"))
            obj.add(MemberRow(unit_rule.AvailableTransportList, "AvailableTransportList"))
            obj.add(MemberRow(str(unit_rule.NumberOfUnitInPack), "NumberOfUnitInPack"))
            obj.add(MemberRow(list(unit_rule.NumberOfUnitInPackXpMultiplier), "NumberOfUnitInPackXpMultiplier"))
        return (self.division.descriptor_path, unit_rule_list)