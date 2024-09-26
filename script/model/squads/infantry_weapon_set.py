from typing import Iterable, Iterator, Self

from model.squads.infantry_weapon import InfantryWeapon
from model.squads.infantry_weapons import InfantryWeapons
from ndf_parse.model import List, ListRow, Object
import utils.ndf.ensure as ensure

class InfantryWeaponSet(object):
    def __init__(self: Self, *weapons: tuple[InfantryWeapon, int]):
        print(str(weapons))
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
    def soldier_count(self: Self) -> int:
        return sum(x.count for x in self.weapons if not x.is_secondary)
    
    @property
    def indices(self: Self) -> Iterable[int]:
        yield from range(self.count)

    @property
    def last(self: Self) -> InfantryWeapons:
        return self.weapons[-1]
    
    @property
    def primaries(self: Self) -> Iterable[InfantryWeapons]:
        yield from [x for x in self.weapons if not x.is_secondary]

    @property
    def secondaries(self: Self) -> Iterable[InfantryWeapons]:
        yield from [x for x in self.weapons if x.is_secondary]

    @property
    def primary_indices(self: Self) -> Iterable[tuple[int, int]]:
        soldier_index = 0
        for weapon in reversed(self.primaries):
            weapon: InfantryWeapons
            for _ in range(weapon.count):
                yield (soldier_index, weapon.index)
                soldier_index += 1

    @property
    def secondary_indices(self: Self) -> Iterable[tuple[int, int]]:
        soldier_index = self.soldier_count - 1
        for weapon in reversed(self.secondaries):
            weapon: InfantryWeapons
            for _ in range(weapon.count):
                yield (soldier_index, weapon.index)
                soldier_index -= 1

    @property
    def assignment(self: Self) -> dict[int, list[int]]:
        result: dict[int, list[int]] = {}
        for s, w in self.primary_indices:
            result[s] = [w]
        for s, w in self.secondary_indices:
            result[s].append(w)
        return result

    def to_weapon_descriptor(self: Self) -> Object:
        return ensure._object('TWeaponManagerModuleDescriptor',
                              Salves=[weapon.salvos for weapon in self.weapons],
                              AlwaysOrientArmorTowardsThreat=False,
                              TurretDescriptorList=[weapon.to_turret_infanterie() for weapon in self.weapons])