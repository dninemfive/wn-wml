import ndf_parse as ndf
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue
from ndf_utils import edit_members, edit_or_read_msg
from typing import Self
from metadata import DivisionMetadata
from message import Message
from ContextManagers.UnitCreationContext import UnitCreationContext
from str_utils import max_len
from ContextManagers.ModCreationContext import ModCreationContext 

PADDING = max_len(rf"GameData\Generated\Gameplay\Decks\Divisions.ndf",
                  rf"GameData\Generated\Gameplay\Decks\DivisionList.ndf",
                  rf"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf",
                  rf"GameData\Generated\Gameplay\Decks\DivisionRules.ndf") + len("Editing ")

class DivisionCreationContext(object):
    def __init__(self: Self, context: ModCreationContext, division: DivisionMetadata):
        self.context = context
        self.division = division
        # todo: cache to ensure this stays constant even if user reorders unit declarations
        self.current_unit_id: int = division.id * 1000

    # https://peps.python.org/pep-0343/
    # https://docs.python.org/3/reference/datamodel.html#context-managers
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @property
    def mod(self: Self) -> Mod:
        return self.context.mod
    
    @property
    def msg(self: Self) -> Message:
        return self.context.root_msg

    @property
    def division_name_internal(self):
        return f'{self.division.dev_short_name}_{self.division.country}_{self.division.short_name}'

    def edit(self: Self, msg: Message, path: str, padding: int = 0) -> ndf.Mod:
        return edit_or_read_msg(self.mod, msg, path, padding, True)
    
    def read(self: Self, msg: Message, path: str, padding: int = 0) -> ndf.Mod:
        return edit_or_read_msg(self.mod, msg, path, padding, False)

    def make_division(self: Self,
                      copy_of: str,
                    **changes: CellValue | None) -> None:
        with self.context.root_msg.nest(f"Making division {self.division.short_name}",
                                        child_padding=PADDING) as msg:
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

    def edit_unit(self: Self, unit_name: str, copy_of: str, showroom_equivalent: str | None = None) -> UnitCreationContext:
        return UnitCreationContext(self, unit_name, copy_of, showroom_equivalent)