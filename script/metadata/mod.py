from dataclasses import dataclass
from metadata.warno import WarnoMetadata
from typing import Self
import os
    
@dataclass
class ModMetadata(object):
    author: str
    name: str
    warno: WarnoMetadata
    version: str
    dev_short_name: str
    localization_prefix: str
    initial_unit_id: int
    
    @property
    def folder_path(self: Self) -> str:
        return os.path.join(self.warno.mods_path, self.name)
    
    @property
    def localization_path(self: Self) -> str:
        return os.path.join(self.folder_path, "GameData", "Localisation", self.name, "UNITS.csv")