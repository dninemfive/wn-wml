from dataclasses import dataclass
from typing import Self

BASE_PATH = rf"GameData\Generated\Gameplay\Decks"
FILES = ["Divisions", "DivisionList", "DeckSerializer", "DivisionRules"]

@dataclass
class DivisionMetadata(object):
    dev_short_name: str
    short_name: str
    country: str
    id: int
    
    @property
    def base_name(self: Self) -> str:
        return f"{self.dev_short_name}_{self.country}_{self.short_name}"

    @property
    def cfg_name(self: Self) -> str:
        return f"'{self.base_name}_multi'"
    
    @property
    def descriptor_name(self: Self) -> str:
        return f'Descriptor_Deck_Division_{self.base_name}_multi'
    
    @property
    def descriptor_path(self: Self) -> str:
        return f'~/{self.descriptor_name}'
    
    @property
    def emblem_namespace(self: Self) -> str:
        return f'Texture_Division_Emblem_{self.base_name}'