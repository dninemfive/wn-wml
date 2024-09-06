from typing import Self
from ndf_parse import Mod
from ndf_parse.model import List
from message import Message, try_nest
from utils.ndf import root_paths

class NdfContext(object):
    def __init__(self: Self, mod: Mod, parent_msg: Message | None, *paths):
        self.mod = mod
        self.parent_msg = parent_msg
        self.paths = paths
       
    def __enter__(self: Self) -> dict[str, List]:
        self.msg = try_nest(self.parent_msg, "Loading ndf files", child_padding=self.msg_length)
        self.msg.__enter__()
        return {x:self.load(x) for x in self.paths}
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        with self.msg.nest("Writing edits", child_padding=self.msg_length) as write_msg:
            for edit in self.mod.edits:
                with write_msg.nest(f"Writing {edit.file_path}") as _:
                    self.mod.write_edit(edit)
        self.msg.__exit__(exc_type, exc_value, traceback)

    def load(self: Self, path: str) -> List:
        with self.msg.nest(f"Loading {path}") as _:
            return self.mod.edit(path).current_tree

    @property
    def msg_length(self: Self):
        return max([len(x) for x in self.paths]) + len("Editing ")