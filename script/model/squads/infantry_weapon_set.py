from typing import Iterable, Self

from model.squads.infantry_weapon import InfantryWeapon
from model.squads.infantry_weapons import InfantryWeapons
from ndf_parse.model import List, ListRow, Object
import utils.ndf.ensure as ensure

class InfantryWeaponSet(object):
    def __init__(self: Self, *weapons: tuple[InfantryWeapon, int]):
        self.weapons: list[InfantryWeapons] = []
        index = 0
        for weapon, ct in weapons:
            self.weapons.append(InfantryWeapons(weapon, ct, index))
            index += 1

    @property
    def count(self: Self) -> int:
        return len(self.weapons)
    
    @property
    def indices(self: Self) -> Iterable[int]:
        yield from range(self.count)

    def to_weapon_descriptor(self: Self) -> Object:
        return ensure._object('TWeaponManagerModuleDescriptor',
                              Salves=[weapon.salvos for weapon in self.weapons],
                              AlwaysOrientArmorTowardsThreat=False,
                              TurretDescriptorList=[weapon.to_turret_infanterie() for weapon in self.weapons])