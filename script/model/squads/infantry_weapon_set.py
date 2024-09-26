from typing import Self

from model.squads.weapon import Weapon, WeaponWithIndex

class InfantryWeaponSet(object):
    def __init__(self: Self, *weapons: tuple[Weapon, int]):
        self.weapons: list[WeaponWithIndex] = [weapons[i][0].with_index(i) for i in range(len(weapons))]
        self.counts = [x[1] for x in weapons]

    @property
    def count(self: Self) -> int:
        return len(self.weapons)
    
    def total_salves_for(self: Self, index: int) -> int:
        return self.counts[index] * self.weapons[index].weapon.salves_per