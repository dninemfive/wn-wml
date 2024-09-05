from typing import Self
from ndf_parse import Mod
from ndf_parse.model import List
from message import Message, try_nest


class NdfFileSet(object):
    def __init__(self: Self, mod: Mod, parent_msg: Message | None, base_path: str = "", *paths: str):
        self.mod = mod
        self.parent_msg = parent_msg
        self.paths = utl.ndf.root_paths(base_path, paths)
        self.loaded_files: dict[str, List] = {}
       
    def __enter__(self: Self) -> list[List]:
        self.msg = try_nest(self.parent_msg, "Loading ndf files", child_padding=self.msg_length)
        self.msg.__enter__()
        return [self.mod.edit(x).current_tree for x in self.paths]
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        with self.msg.nest("Writing edits", child_padding=self.msg_length) as write_msg:
            for edit in self.mod.edits:
                with write_msg.nest(f"Writing {edit.file_path}") as _:
                    self.mod.write_edit(edit)
        self.msg.__exit__(self, exc_type, exc_value, traceback)
        self.loaded_files = {}

    @property
    def msg_length(self: Self):
        return max([len(x) for x in self.paths]) + len("Editing ")