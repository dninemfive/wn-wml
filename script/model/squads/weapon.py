from dataclasses import dataclass
from typing import Literal


@dataclass
class Weapon(object):
    ammo_path: str
    effect_tag: str
    model_path: str
    weapon_type: Literal["'bazooka'", "'grenade'", "'mmg'", "'smg'"] | None = None