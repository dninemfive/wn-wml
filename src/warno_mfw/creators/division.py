from __future__ import annotations

from typing import Self

import warno_mfw.unit_registration.division_unit_registry as ur_dur
import warno_mfw.utils.ndf.edit as edit
from ndf_parse.model import List, ListRow, Map, MapRow
from ndf_parse.model.abc import CellValue
from warno_mfw.hints.paths.GameData.Generated import Gameplay
from warno_mfw.hints.paths.GameData.Generated.Gameplay.Decks import (
    DeckSerializer, DivisionList, DivisionRules, Divisions)
from warno_mfw.metadata.division import DivisionMetadata
from warno_mfw.utils.ndf.decorators import ndf_path
from warno_mfw.utils.types.message import Message


# todo: corresponding wrapper
class DivisionCreator(object):
    def __init__(self: Self,
                 guid: str,
                 copy_of: str,
                 insert_after: str | None,
                 division: DivisionMetadata,
                 units: ur_dur.DivisionUnitRegistry,
                 **changes: CellValue | None):
        self.guid = guid
        self.copy_of = copy_of
        self.division = division
        self.units = units
        self.changes = changes
        self.insert_after = insert_after

    def apply(self: Self, ndf: dict[str, List], msg: Message):
        self.edit_divisions_ndf(ndf, msg)
        self.edit_division_list_ndf(ndf, msg)
        self.edit_division_rules_ndf(ndf, msg)
        self.edit_deck_serializer_ndf(ndf, msg)
        self.units.edit_deck_serializer(ndf, msg)

    @ndf_path(Divisions)
    def edit_divisions_ndf(self: Self, ndf: List):
        copy: ListRow = ndf.by_name(self.copy_of).copy()
        edit.members(copy.value, 
                    DescriptorId = self.guid,
                    CfgName = self.division.cfg_name,
                    **self.changes)
        edit.members(copy.value, PackList=self.units.pack_list())
        copy.namespace = self.division.descriptor_name
        ndf.add(copy)
    
    @ndf_path(DivisionList)
    def edit_division_list_ndf(self: Self, ndf: List):
        division_list: List = ndf.by_name("DivisionList").value.by_member("DivisionList").value
        if self.insert_after is not None:
            index = division_list.find_by_cond(lambda x: x.value == f"~/{self.insert_after}").index
            division_list.insert(index + 1, self.division.descriptor_path)
        else:
            division_list.add(self.division.descriptor_path)

    @ndf_path(DeckSerializer)
    def edit_deck_serializer_ndf(self: Self, ndf: List):
        division_ids: Map = ndf.by_name("DeckSerializer").value.by_member('DivisionIds').value
        division_ids.add(k=self.division.descriptor_name, v=str(self.division.id))

    @ndf_path(DivisionRules)
    def edit_division_rules_ndf(self: Self, ndf: List):   
        division_rules: Map[MapRow] = ndf.by_name("DivisionRules").value.by_member("DivisionRules").value
        division_rules.add(key=self.division.descriptor_path, value=self.units.division_rules())