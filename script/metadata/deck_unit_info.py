from dataclasses import dataclass
from metadata.division import DivisionMetadata
from ndf_parse.model import List, MemberRow, Object
from typing import Self
from utils.ndf import to_List

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
    
class DivisionUnits(object):
    division: DivisionMetadata
    units: list[tuple[tuple[str, int], TDeckUniteRule]]

    def DivisionRules(self: Self) -> tuple[str, Object]:
        unit_rule_list: list[Object] = []
        for _, unit_rule in self.units:
            unit_rule_list.append(unit_rule.to_obj())
        return (self.division.descriptor_path, unit_rule_list)