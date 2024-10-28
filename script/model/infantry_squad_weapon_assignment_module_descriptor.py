from dataclasses import dataclass
from typing import Self
from ndf_parse.model import MapRow, Object
import utils.ndf.ensure as ensure

@dataclass
class TInfantrySquadWeaponAssignmentModuleDescriptor(object):
    InitialSoldiersToTurretIndexMap: dict[int, list[int]]
    @staticmethod
    def from_items(*items: int | list[int]) -> Self:
        result: dict[int, list[int]] = {}
        index = 0
        for item in items:
            if isinstance(item, int):
                item = [item]
            result[index] = item
            index += 1
        return result
    
    @staticmethod
    def from_ndf(ndf: Object) -> Self:
        result: dict[int, list[int]] = {}
        for row in ndf.by_member('InitialSoldiersToTurretIndexMap').value:
            row: MapRow
            result[row.key] = result[[x.value for x in row.value]]
        return result
    
    def to_ndf(self: Self) -> Object:
        return ensure._object('TInfantrySquadWeaponAssignmentModuleDescriptor',
                              InitialSoldiersToTurretIndexMap=self.InitialSoldiersToTurretIndexMap)