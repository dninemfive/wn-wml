from dataclasses import dataclass
from typing import Any, Self
from .._test import GameData
from warno_mfw.utils.ndf._test import GameData

class Folder(object):

    def __init__(self: Self, name: str = '', **attrs: Self | str):
        self.name = name
        self.parent = None
        self.is_frozen = False
        for k, v in attrs:
            setattr(self, k, v)
            if isinstance(v, Folder):
                v.name = k
                v.parent = self
        self.is_frozen = True

    def __setattr__(self, name: str, value: Any) -> None:
        # https://stackoverflow.com/a/74462130
        if self.is_frozen:
            raise AttributeError("Cannot modify a Folder object.")
        super().__setattr__(self, name, value)
    
    @property
    def path(self: Self) -> str:
        if self.parent is None:
            return self.name
        return f'{self.parent.path}/{self.name}'
    
GameData.Generated.Decks.DeckPacks