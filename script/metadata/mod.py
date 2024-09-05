from dataclasses import dataclass
from typing import Self
    
@dataclass
class ModMetadata(object):
    author: str
    name: str
    base_path: str
    version: str

    @property
    def source_path(self: Self):
        return f'{self.base_path}{self.name} (input)'
    
    @property
    def output_path(self: Self):
        return f'{self.base_path}{self.name}'