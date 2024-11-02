import os
from dataclasses import dataclass
from typing import Self

from metadata.warno import WarnoMetadata


@dataclass
class ModMetadata(object):
    author: str
    name: str
    warno: WarnoMetadata
    version: str
    dev_short_name: str
    localization_prefix: str
    
    @property
    def folder_path(self: Self) -> str:
        return os.path.join(self.warno.mods_path, self.name)
    
    @property
    def localization_path(self: Self) -> str:
        return os.path.join(self.folder_path, "GameData", "Localisation", self.name, "UNITS.csv")