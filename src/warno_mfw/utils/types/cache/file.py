import os
from typing import Self, TypeVar

from warno_mfw.utils.io import load, write

from .base import BaseCache

V = TypeVar('V')
DEFAULT_FOLDER = rf"script\_cache"

class FileCache(BaseCache[V]):
    def __init__(self: Self,  name: str, folder: str = DEFAULT_FOLDER):
        self.file_path = os.path.join(folder, f'{name}.cache')

    def _load_data(self: Self) -> dict[str, V]:
        return load(self.file_path, {})

    def _save_data(self: Self, accessed_items: dict[str, V]) -> None:
        write(accessed_items, self.file_path)