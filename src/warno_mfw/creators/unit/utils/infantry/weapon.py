from dataclasses import dataclass
from typing import Self

from warno_mfw.hints import WeaponType
from warno_mfw.hints._validation import _resolve_WeaponType


@dataclass
class InfantryWeapon(object):
    ammo_path: str
    effect_tag: str
    model_path: str
    salvos_per: int
    weapon_type: WeaponType | None = None
    is_secondary: bool = False

    # https://stackoverflow.com/a/51248309
    def __post_init__(self: Self) -> None:
        if self.weapon_type is not None:
            self.weapon_type = _resolve_WeaponType(self.weapon_type)