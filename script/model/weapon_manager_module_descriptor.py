from dataclasses import dataclass
from typing import Self

from ndf_parse.model import List, ListRow, Object

from utils.ndf import ensure

@dataclass
class TWeaponManagerModuleDescriptor(object):
    Salves: list[int]
    AlwaysOrientArmorTowardsThreat: bool
    TurretDescriptorList: list[Object]

    @staticmethod
    def from_ndf(ndf: ListRow | Object) -> Self:
        return TWeaponManagerModuleDescriptor(
            [int(x) for x in ndf.by_member('Salves').value],
            bool(ndf.by_member('AlwaysOrientArmorTowardsThreat')),
            [x for x in ndf.by_member('TurretDescriptorList').value]
        )
    
    def to_ndf(self: Self) -> Object:
        return ensure._object('TWeaponManagerModuleDescriptor',
                              self.Salves,
                              self.AlwaysOrientArmorTowardsThreat,
                              self.TurretDescriptorList)