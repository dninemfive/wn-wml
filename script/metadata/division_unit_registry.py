from dataclasses import dataclass
from message import Message, try_nest
from metadata.division import DivisionMetadata
from metadata.unit import UnitMetadata
from metadata.unit_info import UnitInfo
from metadata.division_rule_lookup import DivisionRuleLookup
from misc.unit_creator import UnitCreator
from model.deck_unite_rule import TDeckUniteRule
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from typing import Self
from utils.ndf import map_from_rows, make_obj, to_List

class DivisionUnitRegistry(object):

    def __init__(self: Self, lookup: DivisionRuleLookup, parent_msg: Message | None = None, *units: UnitInfo):
        self.units: list[UnitInfo] = []
        for unit in units:
            self.register(unit)
        self.lookup = lookup
        self.parent_msg = parent_msg

    def register(self: Self, info: UnitInfo):
        with try_nest(self.parent_msg, f"Registering {info.unit.name}") as _:
            self.units.append(info)

    def register_vanilla(self: Self, unit: str | UnitMetadata, packs: int, override_transports: list[str] | None = None):
        if isinstance(unit, str):
            unit = UnitMetadata(unit)
        with try_nest(self.parent_msg, f"Registering vanilla unit {unit}") as msg:
            unite_rule = self.lookup.look_up(unit.descriptor_path, override_transports)
            if unite_rule is not None:
                self.units.append(UnitInfo.from_deck_unite_rule(unit, packs, unite_rule))
            else:
                with msg.nest("Failed: could not find unit in any division rule") as _:
                    pass

    def pack_list(self: Self) -> Map:
        return map_from_rows(x.pack for x in self.units)
    
    def division_rules(self: Self) -> Object:
        return make_obj('TDeckDivisionRule',
                        UnitRuleList=to_List(*[unit.rule.to_ndf()
                                             for unit
                                             in self.units]))