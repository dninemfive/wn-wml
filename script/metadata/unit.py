from dataclasses import dataclass
from typing import Self

from script.utils.ndf import ensure
from utils.localization import delocalize


@dataclass
class UnitMetadata(object):
    name: str

    @property
    def quoted_name(self: Self) -> str:
        return f"'{self.name}'"
    
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
    def showroom_descriptor_name(self: Self) -> str:
        return f'Descriptor_ShowRoomUnit_{self.name}'

    @property
    def showroom_descriptor_path(self: Self) -> str:
        return f'$/GFX/Unit/{self.showroom_descriptor_name}'
    
    @property
    def deck_pack_descriptor_name(self: Self) -> str:
        return f"Descriptor_Deck_Pack_{self.name}"
    
    @property
    def deck_pack_descriptor_path(self: Self) -> str:
        return f"~/{self.deck_pack_descriptor_name}"
    
    @property
    def tag(self: Self) -> str:
        return f'"UNITE_{self.name}"'
    
    @property
    def button_texture_name(self: Self) -> str:
        return f'Texture_Button_Unit_{self.name}'
    
    @property
    def weapon_descriptor_name(self: Self) -> str:
        return f'WeaponDescriptor_{self.name}'
    
    @property
    def weapon_descriptor_path(self: Self) -> str:
        return f'$/GFX/Weapon/{self.weapon_descriptor_name}'
    
    @staticmethod
    def from_localized_name(prefix: str, localized_name: str, country: str) -> Self:
        return UnitMetadata(f"{prefix}_{delocalize(localized_name)}_{country}")
    
    @staticmethod
    def resolve(val: str | Self) -> Self:
        if isinstance(val, str):
            return UnitMetadata(ensure.no_prefix(val, 'Descriptor_Unit_'))
        if isinstance(val, UnitMetadata):
            return val
        raise TypeError(f'Cannot resolve an object of type {type(val).__name__} to UnitMetadata!')
    
    @staticmethod
    def try_resolve(val: str | Self | None, backup: str | Self) -> Self:
        if val is not None:
            return UnitMetadata.resolve(val)
        return UnitMetadata.resolve(backup)