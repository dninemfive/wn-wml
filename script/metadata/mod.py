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

    @property
    def source_path(self: Self):
        return os.path.join(self.warno.mods_path, f'{self.name} (input)')
    
    @property
    def output_path(self: Self):
        return os.path.join(self.warno.mods_path, self.name)