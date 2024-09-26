from typing import Self

import utils.ndf.ensure as ensure
from constants.ndf import DISPERSION_COLOR, DISPERSION_THICKNESS
from model.squads.infantry_weapon import InfantryWeapon
from ndf_parse.model import Object


class InfantryWeapons(object):
    def __init__(self: Self, weapon: InfantryWeapon, count: int, index: int):
        self.weapon = weapon
        self.index = index
        self.count = count

    @property
    def salvos(self: Self) -> int:
        return self.count * self.weapon.salvos_per

    @property
    def is_secondary(self: Self) -> bool:
        return self.weapon.is_secondary
    
    @property
    def art_index(self: Self) -> int:
        return self.index + 1
    
    def to_mounted_weapon_descriptor(self: Self) -> Object:
        return ensure._object('TMountedWeaponDescriptor',
                              AmmoConsumption_ForInterface=1,
                              Ammunition=self.weapon.ammo_path,
                              AnimateOnlyOneSoldier=self.count==1,
                              DispersionRadiusOffColor=DISPERSION_COLOR,
                              DispersionRadiusOffThickness=DISPERSION_THICKNESS,
                              DispersionRadiusOnColor=DISPERSION_COLOR,
                              DispersionRadiusOnThickness=DISPERSION_THICKNESS,
                              EffectTag=self.weapon.effect_tag,
                              HandheldEquipmentKey=f"'MeshAlternative_{self.art_index}'",
                              NbWeapons=self.count,
                              SalvoStockIndex=self.index,
                              ShowDispersion=False,
                              ShowInInterface=True,
                              WeaponActiveAndCanShootPropertyName=f"'WeaponActiveAndCanShoot_{self.art_index}'",
                              WeaponIgnoredPropertyName = f"'WeaponIgnored_{self.art_index}'",
                              WeaponShootDataPropertyName = [f'"WeaponShootData_0_{self.art_index}"'])
    
    def to_turret_infanterie(self: Self) -> Object:
        return ensure._object('TTurretInfanterieDescriptor',
                              MountedWeaponDescriptorList=[self.to_mounted_weapon_descriptor()],
                              YulBoneOrdinal=self.art_index)