from typing import Iterable, Self

from model.squads.weapon import Weapon, WeaponWithIndex
from ndf_parse.model import List, ListRow, Object
import utils.ndf.ensure as ensure

_DISPERSION_COLOR     = 'RGBA[0,0,0,0]'
_DISPERSION_THICKNESS = -0.1

class InfantryWeaponSet(object):
    def __init__(self: Self, *weapons: tuple[Weapon, int]):
        self.weapons: list[WeaponWithIndex] = [weapons[i][0].with_index(i) for i in range(len(weapons))]
        self.counts = [x[1] for x in weapons]

    @property
    def count(self: Self) -> int:
        return len(self.weapons)
    
    @property
    def indices(self: Self) -> Iterable[int]:
        yield from range(self.count)
    
    def total_salves_for(self: Self, index: int) -> int:
        return self.counts[index] * self.weapons[index].weapon.salves_per
    
    def to_weapon_descriptor(self: Self) -> Object:
        def mounted_weapon_for(weapon: Weapon, index: int, count: int) -> Object:
            return ensure._object('TMountedWeaponDescriptor',
                                  AmmoConsumption_ForInterface=1,
                                  Ammunition=weapon.ammo_path,
                                  AnimateOnlyOneSoldier=count==1,
                                  DispersionRadiusOffColor=_DISPERSION_COLOR,
                                  DispersionRadiusOffThickness=_DISPERSION_THICKNESS,
                                  DispersionRadiusOnColor=_DISPERSION_COLOR,
                                  DispersionRadiusOnThickness=_DISPERSION_THICKNESS,
                                  EffectTag=weapon.effect_tag,
                                  HandheldEquipmentKey=f"'MeshAlternative_{index+1}'",
                                  NbWeapons=count,
                                  SalvoStockIndex=index,
                                  ShowDispersion=False,
                                  ShowInInterface=True,
                                  WeaponActiveAndCanShootPropertyName=f"'WeaponActiveAndCanShoot_{index+1}'",
                                  WeaponIgnoredPropertyName = f"'WeaponIgnored_{index+1}'",
                                  WeaponShootDataPropertyName = [f'"WeaponShootData_0_{index+1}"'])
        def turret_infanterie_for(weapon: WeaponWithIndex, count: int) -> Object:
            return ensure._object('TTurretInfanterieDescriptor',
                                  MountedWeaponDescriptorList=[mounted_weapon_for(weapon.weapon, weapon.index, count)],
                                  YulBoneOrdinal=weapon.index+1)
        result = ensure._object('TWeaponManagerModuleDescriptor',
                                Salves=[self.total_salves_for(i) for i in self.indices],
                                AlwaysOrientArmorTowardsThreat=False,
                                TurretDescriptorList=[turret_infanterie_for(self.weapons[i], self.counts[i]) for i in self.indices])