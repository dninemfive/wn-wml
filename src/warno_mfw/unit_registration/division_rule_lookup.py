from __future__ import annotations

from typing import Self

from metadata.unit import UnitMetadata
from model.deck_unite_rule import TDeckUniteRule
from utils.types.message import Message, try_nest
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object


class DivisionRuleLookup(object):
    def __init__(self: Self, ndf: List, *division_prio: str):
        self.division_rules: Map = ndf.by_name("DivisionRules").value.by_member("DivisionRules").value
        self.division_prio = [f'~/Descriptor_Deck_Division_{x}_multi' for x in division_prio]

    def look_up(self: Self,
                unit: UnitMetadata,
                parent_msg: Message | None = None) -> TDeckUniteRule:
        result = None
        # with try_nest(parent_msg, f"Looking up {unit_descriptor_path} for rules") as msg:
        for division in self.division_prio:
            try:
                unit_rule_list: List = self.division_rules.by_key(division).value.by_member("UnitRuleList").value
                result = unit_rule_list.find_by_cond(lambda x: x.value.by_member("UnitDescriptor").value == unit.descriptor.path).value
            except:
                continue
            if result is not None:
                return TDeckUniteRule.from_ndf(result)
        raise Exception(f"Could not find {unit.descriptor.path} in any of the specified divisions!")