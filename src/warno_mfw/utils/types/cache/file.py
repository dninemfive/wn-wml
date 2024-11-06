import os
from collections import defaultdict
from typing import Self, TypeVar

from warno_mfw.utils.io import load_file, write_file
from warno_mfw.utils.types.message import Message, try_nest

from .base import BaseCache

V = TypeVar('V')
DEFAULT_FOLDER = rf"script\_cache"

class FileCache(BaseCache[V]):
    def __init__(self: Self,  name: str, folder: str = DEFAULT_FOLDER):
        self.file_path = os.path.join(folder, f'{name}.cache')
        self._accessed: defaultdict[str, bool] = defaultdict(lambda: False)        

    def __getitem__(self: Self, key: str) -> V:
        self._accessed[key] = True
        return super().__getitem__(key)
    
    def __setitem__(self: Self, key: str, val: V):
        self._accessed[key] = True
        super().__setitem__(key, val)

    def __contains__(self: Self, key: str) -> bool:
        self._accessed[key] = True
        return super().__contains__(key)

    def load(self: Self, parent_msg: Message | None) -> None:
        with try_nest(parent_msg, self.file_path) as _:
            self._data = load_file(self.file_path, {})

    def save(self: Self, parent_msg: Message | None) -> None:
        with try_nest(parent_msg, self.file_path) as _:
            write_file({k: v for k, v in self._data.items() if self._accessed[k]}, self.file_path)