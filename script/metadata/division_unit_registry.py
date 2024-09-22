from typing import Self

import utils.ndf.ensure as ensure
from constants.ndf_paths import DECK_SERIALIZER, DIVISION_RULES
# from context.mod_creation_context import ModCreationContext
from managers.unit_id import UnitIdManager
from metadata.division import DivisionMetadata
from metadata.division_rule_lookup import DivisionRuleLookup
from metadata.unit import UnitMetadata
from metadata.unit_rules import UnitRules
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from utils.ndf.decorators import ndf_path
from utils.types.message import Message, try_nest


def ensure_unit_path_list(transports: str | list[str] | None) -> list[str] | None:
        if transports is None:
            return None
        if isinstance(transports, str):
            transports = [transports]
        return [ensure.unit_path(x) for x in transports]

class DivisionUnitRegistry(object):
    # ctx: ModCreationContext
    def __init__(self: Self, ctx, metadata: DivisionMetadata, parent_msg: Message | None = None, *division_priorities: str):
        self.metadata = metadata
        self.units: list[UnitRules] = []
        self.parent_msg = parent_msg
        self.unit_ids = UnitIdManager(ctx.unit_id_cache, metadata.id * 1000)
        self.lookup = DivisionRuleLookup(ctx.ndf[DIVISION_RULES], *division_priorities)
    
    @ndf_path(DECK_SERIALIZER)
    def edit_deck_serializer(self: Self, ndf: List):
        unit_ids: Map = ndf.by_name("DeckSerializer").value.by_member('UnitIds').value
        for k, v in self.unit_ids.items:
            unit_ids.add(k=k, v=str(v))

    def register(self: Self, rules: UnitRules, override_transports: str | list[str] | None = None):
        override_transports = ensure_unit_path_list(override_transports)
        if override_transports is not None:
            rules.rule.AvailableTransportList = override_transports
            rules.rule.AvailableWithoutTransport = False
        with try_nest(self.parent_msg, f"Registering {rules.unit.name}") as _:
            self.units.append(rules)
            self.unit_ids.register(rules.unit.descriptor_path)

    def register_vanilla(self: Self, unit: str | UnitMetadata, packs: int, override_transports: str | list[str] | None = None):
        if isinstance(unit, str):
            unit = UnitMetadata(unit)
        override_transports = ensure_unit_path_list(override_transports)
        with try_nest(self.parent_msg, f"Registering vanilla unit {unit}") as msg:
            unite_rule = self.lookup.look_up(unit.descriptor_path, override_transports, msg)
            if unite_rule is not None:
                self.units.append(UnitRules.from_deck_unite_rule(unit, packs, unite_rule))
            else:
                with msg.nest("Failed: could not find unit in any division rule") as _:
                    pass

    def pack_list(self: Self) -> Map:
        return ensure._map(x.pack for x in self.units)
    
    def division_rules(self: Self) -> Object:
        return ensure._object('TDeckDivisionRule',
                            UnitRuleList=[unit.rule.to_ndf()
                                          for unit
                                          in self.units])