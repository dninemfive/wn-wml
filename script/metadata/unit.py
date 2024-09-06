from dataclasses import dataclass
from typing import Self

@dataclass
class UnitMetadata(object):
    name: str
    
    @property
    def class_name_for_debug(self: Self) -> str:
        return f"'Unit_{self.name}'"
    
    @property
    def descriptor_name(self: Self) -> str:
        return f'Descriptor_Unit_{self.name}'
    
    @property
    def descriptor_path(self: Self) -> str:
        return f'$/GFX/Unit/{self.descriptor_name}'
    
    @property
    def showroom_descriptor_path(self: Self) -> str:
        return f'$/GFX/Unit/Descriptor_ShowRoomUnit_{self.name}'