from dataclasses import dataclass
from typing import Self
from message import Message
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, Object
from ndf_parse.model.abc import CellValue
from utils_ndf import edit_members
from utils_str import max_len
    
@dataclass
class ModMetadata(object):
    author: str
    name: str
    base_path: str
    version: str

    @property
    def source_path(self):
        return f'{self.base_path}{self.name} (input)'
    
    @property
    def output_path(self):
        return f'{self.base_path}{self.name}'


DIVISION_PADDING = max_len(rf"GameData\Generated\Gameplay\Decks\Divisions.ndf",
                           rf"GameData\Generated\Gameplay\Decks\DivisionList.ndf",
                           rf"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf",
                           rf"GameData\Generated\Gameplay\Decks\DivisionRules.ndf") + len("Editing ")

@dataclass
class DivisionMetadata(object):
    dev_short_name: str
    short_name: str
    country: str
    id: int
    
    def base_unit_name(self, unit_name: str) -> str:
        return f'Unit_{self.dev_short_name}_{unit_name}_{self.country}'    
    
    @property
    def division_name_internal(self):
        return f'{self.division.dev_short_name}_{self.division.country}_{self.division.short_name}'
    
    def make(self: Self,
             mod: Mod,
             copy_of: str,
           **changes: CellValue | None) -> None:
        with Message(f"Making division {self.division.short_name}",
                                        child_padding=DIVISION_PADDING) as msg:
            ddd_name = f'Descriptor_Deck_Division_{self.division_name_internal}_multi'
            
            with self.edit(msg, rf"GameData\Generated\Gameplay\Decks\Divisions.ndf") as divisions_ndf:
                copy: ListRow = divisions_ndf.by_name(copy_of).copy()
                edit_members(copy.value, 
                            DescriptorId = self.context.generate_guid(ddd_name),
                            CfgName = f"'{self.division_name_internal}_multi'",
                            **changes)
                copy.namespace = ddd_name
                divisions_ndf.add(copy)
                
            with self.edit(msg, rf"GameData\Generated\Gameplay\Decks\DivisionList.ndf") as division_list_ndf:
                division_list: List = division_list_ndf.by_name("DivisionList").value.by_member("DivisionList").value
                division_list.add(f"~/{ddd_name}")
            
            with self.edit(msg, rf"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf") as deck_serializer_ndf:
                division_ids: Map = deck_serializer_ndf.by_name("DeckSerializer").value.by_member('DivisionIds').value
                division_ids.add(k=ddd_name, v=str(self.division.id))
                
            with self.edit(msg, rf"GameData\Generated\Gameplay\Decks\DivisionRules.ndf") as division_rules_ndf:
                division_rules: Map[MapRow] = division_rules_ndf.by_name("DivisionRules").value.by_member("DivisionRules").value
                copy: Object = division_rules.by_key(f"~/{copy_of}").value.copy()
                division_rules.add(k=f'~/{ddd_name}', v=copy)