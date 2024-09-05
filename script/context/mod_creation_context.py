from metadata.division import DivisionMetadata, DIVISION_PADDING
from metadata.mod import ModMetadata
from ndf_parse import Mod
from message import Message, try_nest
from ndf_parse.model import List, ListRow, Map, MapRow, Object
from ndf_parse.model.abc import CellValue
from typing import Self
from utils.io import load, write
from utils.ndf import edit_members, ndf_path
from uuid import uuid4

class ModCreationContext(object):
    """
    Context for creating a WARNO mod, handling things like guid caching (so IDs don't change between builds) and managing the ndf.Mod itself.
    
    Intended to be used in a `with .. as ..` block; see __enter__() and __exit__() for details.
    """
    def __init__(self: Self, metadata: ModMetadata, guid_cache_path: str):
        self.metadata = metadata
        self.mod = Mod(metadata.source_path, metadata.output_path)
        self.guid_cache_path = guid_cache_path

    def __enter__(self: Self):
        """ Allows using this context using a `with` statement, initializing the mod's edits and loading the guid cache. """
        self.mod.check_if_src_is_newer()
        self.guid_cache: dict[str, str] = load(self.guid_cache_path, {})
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        """
        Closes this context at the end of a `with` block, writing out the cache.
        """
        write(self.guid_cache, self.guid_cache_path)

    @ndf_path(rf"GameData\Generated\Gameplay\Decks\Divisions.ndf")
    def edit_divisions_ndf(self: Self, ndf: List, msg: Message, copy_of: str, ddd_name: str, **changes: CellValue | None):
        with msg.nest("edit_divisions_ndf()") as _:
            copy: ListRow = ndf.by_name(copy_of).copy()
            edit_members(copy.value, 
                        DescriptorId = self.generate_guid(ddd_name),
                        CfgName = f"'{self.division_name_internal}_multi'",
                        **changes)
            copy.namespace = ddd_name
            ndf.add(copy)
    
    @ndf_path(rf"GameData\Generated\Gameplay\Decks\DivisionList.ndf")
    def edit_division_list_ndf(self: Self, ndf: List, msg: Message, ddd_name: str):
        division_list: List = ndf.by_name("DivisionList").value.by_member("DivisionList").value
        division_list.add(f"~/{ddd_name}")

    @ndf_path(rf"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf")
    def edit_deck_serializer_ndf(self: Self, ndf: List, msg: Message, ddd_name: str, division_id: int):
        division_ids: Map = ndf.by_name("DeckSerializer").value.by_member('DivisionIds').value
        division_ids.add(k=ddd_name, v=str(division_id))

    @ndf_path(rf"GameData\Generated\Gameplay\Decks\DivisionRules.ndf")
    def edit_division_rules_ndf(self: Self, ndf: List, msg: Message, copy_of: str, ddd_name: str):        
        division_rules: Map[MapRow] = ndf.by_name("DivisionRules").value.by_member("DivisionRules").value
        copy: Object = division_rules.by_key(f"~/{copy_of}").value.copy()
        division_rules.add(k=f'~/{ddd_name}', v=copy)

    def create_division(self: Self, division: DivisionMetadata, copy_of: str, root_msg: Message | None, **changes: CellValue | None) -> None:
        with try_nest(root_msg, 
                      f"Making division {division.short_name}",
                      child_padding=DIVISION_PADDING) as msg:            
            self.edit_divisions_ndf(self.mod, msg, copy_of, division.deck_discriptor_name, **changes)
            self.edit_division_list_ndf(self.mod, msg, division.deck_discriptor_name)
            self.edit_deck_serializer_ndf(self.mod, msg, division.deck_discriptor_name, division.id)
            self.edit_division_rules_ndf(self.mod, msg, copy_of, division.deck_discriptor_name)
    
    def create_units(self: Self): # -> MultipleUnitCreationContext:
        pass

    def generate_guid(self: Self, guid_key: str | None) -> str:
        """ Generates a GUID in the format NDF expects """
        if guid_key in self.guid_cache:
            return self.guid_cache[guid_key]
        result: str = f'GUID:{{{str(uuid4())}}}'
        self.guid_cache[guid_key] = result
        return result