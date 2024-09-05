from script.metadata.mod import DivisionMetadata, ModMetadata
from typing import Self
from uuid import uuid4
from utils_io import load, write
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue
from message import Message
from script.metadata.mod import DivisionMetadata
from typing import Self
from utils_ndf import edit_members, edit_or_read_file_with_msg
from utils_str import max_len

class ModCreationContext(object):
    """ Context for creating a WARNO mod, handling things like guid caching (so IDs don't change between builds) and managing the ndf.Mod itself """
    def __init__(self: Self, metadata: ModMetadata, guid_cache_path: str):
        self.metadata = metadata
        self.mod = Mod(metadata.source_path, metadata.output_path)
        self.guid_cache_path = guid_cache_path
        self.guid_cache: dict[str, str] = load(guid_cache_path, {})

    def __enter__(self: Self):
        self.mod.check_if_src_is_newer()
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        write(self.guid_cache, self.guid_cache_path)

    def create_division(self: Self, division: DivisionMetadata, copy_of: str, **changes: CellValue | None) -> None:
        division.make(self.mod, copy_of, changes)
    
    def create_units(self: Self): # -> MultipleUnitCreationContext:
        pass

    def generate_guid(self: Self, guid_key: str | None) -> str:
        """ Generates a GUID in the format NDF expects """
        if guid_key in self.guid_cache:
            return self.guid_cache[guid_key]
        result: str = f'GUID:{{{str(uuid4())}}}'
        self.guid_cache[guid_key] = result
        return result