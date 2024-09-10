from dataclasses import dataclass
from message import Message, try_nest
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
    def from_vanilla(unit: UnitMetadata, num_packs: int, division_rules_ndf: List, *divisions_for_rule: str) -> Self:
        division_rules_ndf

UNITE_RULE = 'TDeckUniteRule'
KEY_AVAILABLE_TRANSPORT_LIST = 'AvailableTransportList'
KEY_UNIT_DESCRIPTOR = 'UnitDescriptor'
KEY_AVAILABLE_WITHOUT_TRANSPORT = 'AvailableWithoutTransport'
KEY_NUMBER_OF_UNIT_IN_PACK = 'NumberOfUnitInPack'
KEY_NUMBER_OF_UNIT_IN_PACK_XP_MULTIPLIER = 'NumberOfUnitInPackXPMultiplier'
@dataclass
class TDeckUniteRule(object):
    UnitDescriptor: str
    AvailableWithoutTransport: bool
    AvailableTransportList: list[str] | None
    NumberOfUnitInPack: int
    NumberOfUnitInPackXPMultiplier: tuple[float, float, float, float]

    @staticmethod
    def from_ndf(ndf: Object) -> Self:
        if ndf.type is not (None or UNITE_RULE):
            raise TypeError
        transports: List | None = None
        try:
            transports = ndf.by_member(KEY_AVAILABLE_TRANSPORT_LIST).value
        except:
            pass
        return TDeckUniteRule(
            ndf.by_member(KEY_UNIT_DESCRIPTOR).value,
            ndf.by_member(KEY_AVAILABLE_WITHOUT_TRANSPORT).value,
            transports,
            ndf.by_member(KEY_NUMBER_OF_UNIT_IN_PACK).value,
            ndf.by_member(KEY_NUMBER_OF_UNIT_IN_PACK_XP_MULTIPLIER)
        )

    def to_ndf(self: Self) -> Object:
        result = Object(UNITE_RULE)
        result.add(MemberRow(self.UnitDescriptor, KEY_UNIT_DESCRIPTOR))
        result.add(MemberRow(str(self.AvailableWithoutTransport), KEY_AVAILABLE_WITHOUT_TRANSPORT))
        if(self.AvailableTransportList is not None):
            result.add(MemberRow(to_List(*self.AvailableTransportList), KEY_AVAILABLE_TRANSPORT_LIST))
        result.add(MemberRow(str(self.NumberOfUnitInPack), KEY_NUMBER_OF_UNIT_IN_PACK))
        result.add(MemberRow(to_List(*[str(x) for x in self.NumberOfUnitInPackXPMultiplier]), KEY_NUMBER_OF_UNIT_IN_PACK_XP_MULTIPLIER))
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
    
class DivisionRuleLookup(object):
    def __init__(self: Self, ndf: List, *division_prio: str):
        self.division_rules: Map = ndf.by_name("DivisionRules").value.by_member("DivisionRules").value
        self.division_prio = division_prio

    def look_up(self: Self, unit_descriptor_path: str) -> TDeckUniteRule | None:
        result = None
        unit_rule_list: List
        for division in self.division_prio:
            try:
                unit_rule_list = self.division_rules.by_key(division).value
                result = unit_rule_list.find_by_cond(lambda x: x.by_member("UnitDescriptor").value == unit_descriptor_path).value
            except:
                continue
            if result is not None:
                return TDeckUniteRule.from_ndf(result)
        return result

class DivisionUnits(object):

    def __init__(self: Self, lookup: DivisionRuleLookup, parent_msg: Message | None = None, *units: UnitInfo):
        self.units: list[UnitInfo] = []
        for unit in units:
            self.register(unit)
        self.lookup = lookup
        self.parent_msg = parent_msg

    def register(self: Self, info: UnitInfo):
        with try_nest(self.parent_msg, f"Registering {info.unit.name}") as _:
            self.units.append(info)

    def reg_vanilla(self: Self, unit: str | UnitMetadata):
        if isinstance(unit, str):
            unit = UnitMetadata(unit)
        with try_nest(self.parent_msg, f"Registering vanilla unit {unit}") as msg:
            unite_rule = TDeckUniteRule.from_ndf(self.lookup.look_up(unit.descriptor_path))
            if unite_rule is not None:
                self.units.append(unite_rule)
            else:
                with msg.nest("Failed: could not find unit in any division rule") as _:
                    pass

    def pack_list(self: Self) -> Map:
        return map_from_rows(x.pack for x in self.units)
    
    def division_rules(self: Self) -> Object:
        return make_obj('TDeckDivisionRule',
                        UnitRuleList=to_List(unit.rule.to_obj()
                                             for unit
                                             in self.units))