import os
from dataclasses import dataclass
from typing import Self


@dataclass
class WarnoMetadata(object):
    base_path: str

    @property
    def mods_path(self: Self) -> str:
        return os.path.join(self.base_path, 'Mods')
    
    @property
    def scripts_path(self: Self) -> str:
        return os.path.join(self.mods_path, 'Utils', 'Scripts')