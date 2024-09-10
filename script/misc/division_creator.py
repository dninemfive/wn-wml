from typing import Self
from message import Message, try_nest
from metadata.deck_unit_info import DivisionUnitRegistry
from metadata.division import DivisionMetadata
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue
from utils.ndf import edit_members, make_obj, ndf_path

class DivisionCreator(object):
    def __init__(self: Self, guid: str, copy_of: str, insert_after: str | None, division: DivisionMetadata, units: DivisionUnitRegistry, **changes: CellValue | None):
        self.guid = guid
        self.copy_of = copy_of
        self.division = division
        self.units = units
        self.changes = changes
        self.insert_after = insert_after

    @property
    def msg_length(self: Self) -> int:
        return max([len(prop._ndf_path) for prop in dir(self) if hasattr(prop, "_ndf_path")])

    def apply(self: Self, ndf: dict[str, List], msg: Message):
        # for fn on class with ndf_path decorator,
        #   fn()
        self.edit_divisions_ndf(ndf, msg)
        self.edit_division_list_ndf(ndf, msg)
        self.edit_division_rules_ndf(ndf, msg)
        self.edit_deck_serializer_ndf(ndf, msg)

    @ndf_path(rf"GameData\Generated\Gameplay\Decks\Divisions.ndf")
    def edit_divisions_ndf(self: Self, ndf: List):
        copy: ListRow = ndf.by_name(self.copy_of).copy()
        edit_members(copy.value, 
                    DescriptorId = self.guid,
                    CfgName = self.division.cfg_name,
                    **self.changes)
        edit_members(copy.value, PackList=self.units.pack_list())
        copy.namespace = self.division.descriptor_name
        ndf.add(copy)
    
    @ndf_path(rf"GameData\Generated\Gameplay\Decks\DivisionList.ndf")
    def edit_division_list_ndf(self: Self, ndf: List):
        division_list: List = ndf.by_name("DivisionList").value.by_member("DivisionList").value
        if self.insert_after is not None:
            index = division_list.find_by_cond(lambda x: x.value == f"~/{self.insert_after}").index
            division_list.insert(index + 1, self.division.descriptor_path)
        else:
            division_list.add(self.division.descriptor_path)

    @ndf_path(rf"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf")
    def edit_deck_serializer_ndf(self: Self, ndf: List):
        division_ids: Map = ndf.by_name("DeckSerializer").value.by_member('DivisionIds').value
        division_ids.add(k=self.division.descriptor_name, v=str(self.division.id))

    @ndf_path(rf"GameData\Generated\Gameplay\Decks\DivisionRules.ndf")
    def edit_division_rules_ndf(self: Self, ndf: List):   
        division_rules: Map[MapRow] = ndf.by_name("DivisionRules").value.by_member("DivisionRules").value
        division_rules.add(key=self.division.descriptor_path, value=self.units.division_rules())