from dataclasses import dataclass
from typing import Self
from message import Message
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, Object
from ndf_parse.model.abc import CellValue
from utils.ndf import edit_members
from utils.misc import max_len
from context.ndf_file_set import NdfFileSet

DIVISION_PADDING = max_len(rf"GameData\Generated\Gameplay\Decks\Divisions.ndf",
                           rf"GameData\Generated\Gameplay\Decks\DivisionList.ndf",
                           rf"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf",
                           rf"GameData\Generated\Gameplay\Decks\DivisionRules.ndf") + len("Editing ")

BASE_PATH = rf"GameData\Generated\Gameplay\Decks"
FILES = ["Divisions", "DivisionList", "DeckSerializer", "DivisionRules"]

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
            
            def edit(path: str) -> Mod:
                with msg.nest(path) as _:
                    return mod.edit(path)

            ddd_name = f'Descriptor_Deck_Division_{self.division_name_internal}_multi'

            with NdfFileSet(mod, msg, BASE_PATH, *FILES) as files:
                pass
            
            with edit(rf"GameData\Generated\Gameplay\Decks\Divisions.ndf") as divisions_ndf:
                copy: ListRow = divisions_ndf.by_name(copy_of).copy()
                edit_members(copy.value, 
                            DescriptorId = self.context.generate_guid(ddd_name),
                            CfgName = f"'{self.division_name_internal}_multi'",
                            **changes)
                copy.namespace = ddd_name
                divisions_ndf.add(copy)
                
            with edit(rf"GameData\Generated\Gameplay\Decks\DivisionList.ndf") as division_list_ndf:
                division_list: List = division_list_ndf.by_name("DivisionList").value.by_member("DivisionList").value
                division_list.add(f"~/{ddd_name}")
            
            with edit(rf"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf") as deck_serializer_ndf:
                division_ids: Map = deck_serializer_ndf.by_name("DeckSerializer").value.by_member('DivisionIds').value
                division_ids.add(k=ddd_name, v=str(self.division.id))
                
            with edit(rf"GameData\Generated\Gameplay\Decks\DivisionRules.ndf") as division_rules_ndf:
                division_rules: Map[MapRow] = division_rules_ndf.by_name("DivisionRules").value.by_member("DivisionRules").value
                copy: Object = division_rules.by_key(f"~/{copy_of}").value.copy()
                division_rules.add(k=f'~/{ddd_name}', v=copy)