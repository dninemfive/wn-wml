from dataclasses import dataclass
from message import Message, try_nest
from metadata.division import DivisionMetadata
from metadata.unit import UnitMetadata
from misc.unit_creator import UnitCreator
from model.deck_unite_rule import TDeckUniteRule
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from typing import Self
from utils.ndf import map_from_rows, make_obj, to_List

class DivisionRuleLookup(object):
    def __init__(self: Self, ndf: List, *division_prio: str):
        self.division_rules: Map = ndf.by_name("DivisionRules").value.by_member("DivisionRules").value
        self.division_prio = [f'~/Descriptor_Deck_Division_{x}_multi' for x in division_prio]

    def look_up(self: Self, unit_descriptor_path: str) -> TDeckUniteRule | None:
        print(f"look_up({unit_descriptor_path})")
        result = None
        unit_rule_list: List
        for division in self.division_prio:
            print(f'\t{division}')
            try:
                unit_rule_list: list = self.division_rules.by_key(division).value.by_member("UnitRuleList").value
                # print(str(unit_rule_list))
                result = unit_rule_list.find_by_cond(lambda x: x.value.by_member("UnitDescriptor").value == unit_descriptor_path).value
            except:
                # print("\tcontinue")
                continue
            if result is not None:
                print("RESULT:")
                print(result)
                result = TDeckUniteRule.from_ndf(result)
                print(str(result))
                return result
        return result