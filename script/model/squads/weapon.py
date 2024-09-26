from dataclasses import dataclass
from typing import Literal, Self

class WeaponWithIndex(object):
    # weapon: Weapon
    def __init__(self: Self, weapon, index: int):
        self.weapon = weapon
        self.index = index

@dataclass
class Weapon(object):
    ammo_path: str
    effect_tag: str
    model_path: str
    salves_per: int
    weapon_type: Literal["'bazooka'", "'grenade'", "'mmg'", "'smg'"] | None = None

    def with_index(self: Self, index: int) -> WeaponWithIndex:
        return WeaponWithIndex(self, index)