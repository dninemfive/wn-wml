from dataclasses import dataclass
from typing import Self
from message import Message
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, Object
from ndf_parse.model.abc import CellValue
from utils.ndf import edit_members
from utils.misc import max_len

DIVISION_PADDING = max_len(rf"GameData\Generated\Gameplay\Decks\Divisions.ndf",
                           rf"GameData\Generated\Gameplay\Decks\DivisionList.ndf",
                           rf"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf",
                           rf"GameData\Generated\Gameplay\Decks\DivisionRules.ndf") + len("Editing ")

BASE_PATH = rf"GameData\Generated\Gameplay\Decks"
FILES = ["Divisions", "DivisionList", "DeckSerializer", "DivisionRules"]

@dataclass
class DivisionMetadata(object):
    dev_short_name: str
    short_name: str
    country: str
    id: int
    
    @property
    def cfg_name(self: Self) -> str:
        return f"'{self.dev_short_name}_{self.country}_{self.short_name}_multi'"
    
    @property
    def descriptor_name(self: Self) -> str:
        return f'Descriptor_Deck_Division_{self.cfg_name}_multi'
    
    @property
    def descriptor_path(self: Self) -> str:
        return f'~/{self.descriptor_name}'