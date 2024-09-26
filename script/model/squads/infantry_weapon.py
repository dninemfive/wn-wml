from dataclasses import dataclass
from typing import Literal, Self

from utils.ndf import ensure

type InputWeaponType    = Literal['bazooka', 'grenade', 'mmg', 'smg']
type WeaponType         = Literal["'bazooka'", "'grenade'", "'mmg'", "'smg'"]

@dataclass
class InfantryWeapon(object):
    ammo_path: str
    effect_tag: str
    model_path: str
    salvos_per: int
    weapon_type: InputWeaponType | WeaponType | None = None
    is_secondary: bool = False

    # https://stackoverflow.com/a/51248309
    def __post_init__(self: Self) -> None:
        if self.weapon_type is not None:
            self.weapon_type = ensure.quoted(self.weapon_type, "'")