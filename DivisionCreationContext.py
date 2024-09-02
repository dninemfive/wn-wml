import ndf_parse as ndf
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue
from ndf_utils import edit_members
from io_utils import load, write
from uuid import uuid4
from typing import Self
from metadata import DivisionMetadata
from message import Message
from UnitCreationContext import UnitCreationContext
from str_utils import max_len

class DivisionCreationContext(object):
    def __init__(self: Self, mod: ndf.Mod, division: DivisionMetadata, guid_cache_path: str):
        self.mod = mod
        self.division = division
        self.guid_cache_path = guid_cache_path
        self.guid_cache: dict[str, str] = load(guid_cache_path, {})
        # todo: cache to ensure this stays constant even if user reorders unit declarations
        self.current_unit_id: int = division.id * 1000

    # https://peps.python.org/pep-0343/
    # https://docs.python.org/3/reference/datamodel.html#context-managers
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        write(self.guid_cache, self.guid_cache_path)

    @property
    def division_name_internal(self):
        return f'{self.division.dev_short_name}_{self.division.short_name}_{self.division.country}'

    def generate_guid(self: Self, guid_key: str | None) -> str:
        """ Generates a GUID in the format NDF expects """
        if guid_key in self.guid_cache:
            return self.guid_cache[guid_key]
        result: str = f'GUID:{{{str(uuid4())}}}'
        self.guid_cache[guid_key] = result
        return result
    
    def edit(self: Self, msg: Message, path: str, padding: int = 0) -> ndf.Mod:
        with msg.nest(f'Editing {path}', padding) as _:
            return self.mod.edit(path)

    def make_division(self: Self,
                      copy_of: str,
                    **changes: CellValue | None) -> None:
        with Message(f"Making division {self.division.short_name}",
                     child_padding=max_len(rf'GameData\Generated\Gameplay\Decks\.ndf', 
                                           'Divisions', 
                                           'DivisionList', 
                                           'DeckSerializer', 
                                           'DivisionRules')) as msg:
            ddd_name = f'Descriptor_Deck_Division_{self.division_name_internal}_multi'
            
            with self.edit(msg, r"GameData\Generated\Gameplay\Decks\Divisions.ndf") as divisions_ndf:
                copy: ListRow = divisions_ndf.by_name(copy_of).copy()
                edit_members(copy.value, 
                            DescriptorId = self.generate_guid(ddd_name),
                            CfgName = f"'{self.division_name_internal}_multi'",
                            **changes)
                copy.namespace = ddd_name
                divisions_ndf.add(copy)
                
            with self.edit(msg, r"GameData\Generated\Gameplay\Decks\DivisionList.ndf") as division_list_ndf:
                division_list: List = division_list_ndf.by_name("DivisionList").value.by_member("DivisionList").value
                division_list.add(f"~/{ddd_name}")
            
            with self.edit(msg, r"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf") as deck_serializer_ndf:
                division_ids: Map = deck_serializer_ndf.by_name("DeckSerializer").value.by_member('DivisionIds').value
                division_ids.add(k=ddd_name, v=str(self.division.id))
                
            with self.edit(msg, r"GameData\Generated\Gameplay\Decks\DivisionRules.ndf") as division_rules_ndf:
                division_rules: Map[MapRow] = division_rules_ndf.by_name("DivisionRules").value.by_member("DivisionRules").value
                copy: Object = division_rules.by_key(f"~/{copy_of}").value.copy()
                division_rules.add(k=f'~/{ddd_name}', v=copy)

    def edit_unit(self: Self, unit_name: str, copy_of: str, showroom_equivalent: str | None = None) -> UnitCreationContext:
        return UnitCreationContext(self, unit_name, copy_of, showroom_equivalent)