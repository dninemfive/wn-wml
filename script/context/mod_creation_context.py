from metadata.division import DivisionMetadata
from metadata.mod import ModMetadata
from ndf_parse import Mod
from message import Message
from ndf_parse.model import List, ListRow
from ndf_parse.model.abc import CellValue
from typing import Self
from utils.io import load, write
from utils.ndf import edit_members, edit_or_read_file_with_msg, ndf_path
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
    def edit_divisions_ndf(ndf: List, msg: Message):
        copy: ListRow = divisions_ndf.by_name(copy_of).copy()
        edit_members(copy.value, 
                    DescriptorId = self.generate_guid(ddd_name),
                    CfgName = f"'{self.division_name_internal}_multi'",
                    **changes)
        copy.namespace = ddd_name
        divisions_ndf.add(copy)

    def create_division(self: Self, division: DivisionMetadata, copy_of: str, **changes: CellValue | None) -> None:
        with Message(f"Making division {self.division.short_name}",
                                        child_padding=DIVISION_PADDING) as msg:
            
            def edit(path: str) -> Mod:
                with msg.nest(path) as _:
                    return mod.edit(path)

            ddd_name = f'Descriptor_Deck_Division_{self.division_name_internal}_multi'
            
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
    
    def create_units(self: Self): # -> MultipleUnitCreationContext:
        pass

    def generate_guid(self: Self, guid_key: str | None) -> str:
        """ Generates a GUID in the format NDF expects """
        if guid_key in self.guid_cache:
            return self.guid_cache[guid_key]
        result: str = f'GUID:{{{str(uuid4())}}}'
        self.guid_cache[guid_key] = result
        return result