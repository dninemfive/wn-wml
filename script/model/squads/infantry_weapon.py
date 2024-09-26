from dataclasses import dataclass
from typing import Self

from constants.primitive_types import InputWeaponType, WeaponType
from utils.ndf import ensure


@dataclass
class InfantryWeapon(object):
    ammo_path: str
    effect_tag: str
    model_path: str
    salvos_per: int
    weapon_type: str | None = None
    is_secondary: bool = False

    # https://stackoverflow.com/a/51248309
    def __post_init__(self: Self) -> None:
        if self.weapon_type is not None:
            self.weapon_type = ensure.literal(self.weapon_type, WeaponType)