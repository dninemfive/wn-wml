from typing import Self

from constants.ndf_paths import DECK_SERIALIZER, DIVISION_RULES
# from context.mod_creation_context import ModCreationContext
from managers.unit_id import UnitIdManager
from metadata.division import DivisionMetadata
from metadata.division_rule_lookup import DivisionRuleLookup
from metadata.unit import UnitMetadata
from metadata.unit_info import UnitRules
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from utils.ndf import ensure_unit_path, make_obj, map_from_rows, ndf_path, to_List
from utils.types.message import Message, try_nest


def ensure_unit_path_list(transports: str | list[str] | None) -> list[str] | None:
        if transports is None:
            return None
        if isinstance(transports, str):
            transports = [transports]
        return [ensure_unit_path(x) for x in transports]

class DivisionUnitRegistry(object):
    # ctx: ModCreationContext
    def __init__(self: Self, ctx, metadata: DivisionMetadata, parent_msg: Message | None = None, *division_priorities: str):
        self.metadata = metadata
        self.units: list[UnitRules] = []
        self.parent_msg = parent_msg
        self.unit_ids = UnitIdManager(ctx.unit_id_cache, metadata.id * 1000)
        self.lookup = DivisionRuleLookup(ctx.ndf[DIVISION_RULES], division_priorities)
    
    @ndf_path(DECK_SERIALIZER)
    def edit_deck_serializer(self: Self, ndf: List):
        unit_ids: Map = ndf.by_name("DeckSerializer").value.by_member('UnitIds').value
        for k, v in self.unit_ids:
            unit_ids.add(k=k, v=v)

    def register(self: Self, info: UnitRules, override_transports: str | list[str] | None = None):
        override_transports = ensure_unit_path_list(override_transports)
        if override_transports is not None:
            info.rule.AvailableTransportList = override_transports
            info.rule.AvailableWithoutTransport = False
        with try_nest(self.parent_msg, f"Registering {info.unit.name}") as _:
            self.units.append(info)
            self.unit_ids.register(info.unit.descriptor_name)

    def register_vanilla(self: Self, unit: str | UnitMetadata, packs: int, override_transports: str | list[str] | None = None):
        if isinstance(unit, str):
            unit = UnitMetadata(unit)
        override_transports = ensure_unit_path_list(override_transports)
        with try_nest(self.parent_msg, f"Registering vanilla unit {unit}") as msg:
            unite_rule = self.lookup.look_up(unit.descriptor_path, override_transports)
            if unite_rule is not None:
                self.units.append(UnitRules.from_deck_unite_rule(unit, packs, unite_rule))
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