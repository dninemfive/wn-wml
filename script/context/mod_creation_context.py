from typing import Self
from metadata.division import DivisionMetadata
from metadata.mod import ModMetadata
from misc.division_creator import DivisionCreator
from ndf_parse import Mod
from ndf_parse.model import List
from ndf_parse.model.abc import CellValue
from message import Message, try_nest
from utils.ndf import root_paths
import utils.io as io
from uuid import uuid4

class ModCreationContext(object):
    @property
    def prefix(self: Self) -> str:
        return self.metadata.dev_short_name

    @property
    def msg_length(self: Self):
        return max([len(x) for x in self.paths]) + len("Editing ")
    
    def __init__(self: Self, metadata: ModMetadata, root_msg: Message | None, *ndf_paths: str):
        self.metadata = metadata
        self.mod = Mod(metadata.source_path, metadata.output_path)
        self.root_msg = root_msg
        self.paths = ndf_paths
       
    def __enter__(self: Self) -> Self:
        self.mod.check_if_src_is_newer()
        self.guid_cache: dict[str, str] = io.load(self.metadata.guid_cache_path, {})
        self.msg = try_nest(self.root_msg, "Loading ndf files", child_padding=self.msg_length)
        self.msg.__enter__()
        self.ndf = {x:self.load_ndf(x) for x in self.paths}
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        with self.msg.nest("Writing edits", child_padding=self.msg_length) as write_msg:
            for edit in self.mod.edits:
                with write_msg.nest(f"Writing {edit.file_path}") as _:
                    self.mod.write_edit(edit)
        with self.msg.nest("Saving GUID cache") as _:
            io.write(self.guid_cache, self.metadata.guid_cache_path)
        self.msg.__exit__(exc_type, exc_value, traceback)
        self.guid_cache = None
    
    def load_ndf(self: Self, path: str) -> List:
        with self.msg.nest(f"Loading {path}") as _:
            return self.mod.edit(path).current_tree
    
    def create_division(self: Self, division: DivisionMetadata, copy_of: str, root_msg: Message | None, **changes: CellValue | None) -> None:
        with try_nest(root_msg, 
                      f"Making division {division.short_name}",
                      child_padding=self.msg_length) as msg:
            DivisionCreator(self.generate_guid(division.descriptor_name), copy_of, division, **changes).apply(self.ndf, msg)

    def generate_guid(self: Self, guid_key: str) -> str:
        """ Generates a GUID in the format NDF expects """
        if guid_key in self.guid_cache:
            return self.guid_cache[guid_key]
        result: str = f'GUID:{{{str(uuid4())}}}'
        self.guid_cache[guid_key] = result
        return result