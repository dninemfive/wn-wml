import os
from typing import Self, TypeVar

from warno_mfw.utils.io import load_file, write_file

from .base import BaseCache

V = TypeVar('V')
DEFAULT_FOLDER = rf"script\_cache"

class FileCache(BaseCache[V]):
    def __init__(self: Self,  name: str, folder: str = DEFAULT_FOLDER):
        self.file_path = os.path.join(folder, f'{name}.cache')

    def load(self: Self) -> dict[str, V]:
        return load_file(self.file_path, {})

    def _save_data(self: Self, accessed_items: dict[str, V]) -> None:
        write_file(accessed_items, self.file_path)