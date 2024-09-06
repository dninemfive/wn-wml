from metadata.division import DivisionMetadata, DIVISION_PADDING
from metadata.mod import ModMetadata
from ndf_parse import Mod
from message import Message, try_nest
from misc.division_creator import DivisionCreator
from ndf_parse.model import List, ListRow, Map, MapRow, Object
from ndf_parse.model.abc import CellValue
from typing import Self
from utils.io import load, write
from utils.ndf import edit_members, load_ndf_path
from uuid import uuid4

class ModCreationContext(object):
    """
    Context for creating a WARNO mod, handling things like guid caching (so IDs don't change between builds) and managing the ndf.Mod itself.
    
    Intended to be used in a `with .. as ..` block; see __enter__() and __exit__() for details.
    """
    def __init__(self: Self, metadata: ModMetadata, guid_cache_path: str = "guid_cache.txt"):
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
        with Message("Saving GUID cache") as _:
            write(self.guid_cache, self.guid_cache_path)
        with Message("Saving NDF edits") as _:
            for edit in self.mod.edits:
                self.mod.write_edit(edit)

    @property
    def prefix(self: Self) -> str:
        return self.metadata.dev_short_name

    def create_division(self: Self, division: DivisionMetadata, copy_of: str, root_msg: Message | None, **changes: CellValue | None) -> None:
        with try_nest(root_msg, 
                      f"Making division {division.short_name}",
                      child_padding=DIVISION_PADDING) as msg:
            DivisionCreator(self.generate_guid(division.descriptor_name), copy_of, division, **changes).apply(self.mod, msg)

    def generate_guid(self: Self, guid_key: str) -> str:
        """ Generates a GUID in the format NDF expects """
        if guid_key in self.guid_cache:
            return self.guid_cache[guid_key]
        result: str = f'GUID:{{{str(uuid4())}}}'
        self.guid_cache[guid_key] = result
        return result