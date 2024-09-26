from typing import Iterable, Iterator, Self

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

    def __iter__(self: Self) -> Iterator[InfantryWeapons]:
        yield from self.weapons

    @property
    def count(self: Self) -> int:
        return len(self.weapons)
    
    @property
    def indices(self: Self) -> Iterable[int]:
        yield from range(self.count)

    @property
    def last(self: Self) -> InfantryWeapons:
        return self.weapons[-1]
    
    @property
    def primaries_in_reverse_order(self: Self) -> Iterable[InfantryWeapons]:
        yield from reversed(x for x in self.weapons if not x.is_secondary)

    @property
    def secondaries_in_order(self: Self) -> Iterable[InfantryWeapons]:
        yield from [x for x in self.weapons if x.is_secondary]

    def to_weapon_descriptor(self: Self) -> Object:
        return ensure._object('TWeaponManagerModuleDescriptor',
                              Salves=[weapon.salvos for weapon in self.weapons],
                              AlwaysOrientArmorTowardsThreat=False,
                              TurretDescriptorList=[weapon.to_turret_infanterie() for weapon in self.weapons])