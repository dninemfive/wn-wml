from typing import Self

from ndf_parse import Mod
from ndf_parse.model import List

from warno_mfw.utils.types.message import Message, try_nest

from .base import BaseCache

class NdfCache(BaseCache[List]):
    def __init__(self: Self, mod: Mod, msg: Message | None = None):
        super().__init__()
        self._mod = mod
        self._msg = msg

    def __getitem__(self: Self, key: str) -> List:
        if key not in self:
            with try_nest(self._msg, f"Loading {key}") as _:
                self._data[key] = self._mod.edit(key).current_tree
        return super().__getitem__(key)

    def _load_data(self: Self) -> dict[str, List]:
        return {}

    def _save_data(self: Self, accessed_items: dict[str, List]) -> None:
        pass