from typing import Self

from ndf_parse import Mod
from ndf_parse.model import List

from warno_mfw.utils.types.message import Message, try_nest

from .base import BaseCache

class NdfCache(BaseCache[List]):
    def __init__(self: Self, mod: Mod):
        super().__init__()
        self._mod = mod

    def __getitem__(self: Self, key: str) -> List:
        if key not in self:
            # TODO: with #30, message here
            self._data[key] = self._mod.edit(key).current_tree
        return super().__getitem__(key)

    def _load_data(self: Self, _: Message | None = None) -> dict[str, List]:
        return {}

    def _save_data(self: Self, accessed_items: dict[str, List], parent_msg: str | None = None) -> None:
        for edit in self._mod.edits:
            with try_nest(parent_msg, f"Writing {edit.file_path}") as _:
                self._mod.write_edit(edit)