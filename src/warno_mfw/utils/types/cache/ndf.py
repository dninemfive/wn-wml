from typing import Self

from ndf_parse import Mod
from ndf_parse.model import List

from warno_mfw.utils.types.message import Message, try_nest

from .base import BaseCache

class NdfCache(BaseCache[List]):
    def __init__(self: Self, mod: Mod):
        super().__init__()
        self._mod = mod
        self._data = {}

    def __getitem__(self: Self, key: str) -> List:
        if key not in self:
            # TODO: with #30, message here
            with try_nest(None, f'Loading ndf {key}') as _:
                self._data[key] = self._mod.edit(key).current_tree
        return super().__getitem__(key)

    def load(self: Self, _: Message | None = None) -> None:
        pass

    def save(self: Self, parent_msg: str | None = None) -> None:
        for edit in sorted(self._mod.edits, key=lambda x: x.file_path):
            with try_nest(parent_msg, f"Writing {edit.file_path}") as _:
                self._mod.write_edit(edit)