from typing import Self

import warno_mfw.utils.ndf.ensure as ensure
from ndf_parse.model import Object

from ._abc import WeaponDepictionOperator


class DepictionOperator_WeaponMissileCarriageFire(WeaponDepictionOperator):
    def __init__(self: Self, index: int, connoisseur_name: str, weapon_index: int | None = None):
        super().__init__(index)
        self.connoisseur_name = connoisseur_name
        self.weapon_index = weapon_index if weapon_index is not None else index

    def to_ndf(self: Self) -> Object:
        return ensure.NdfObject(
            'DepictionOperator_WeaponMissileCarriageFire',
            Connoisseur=self.connoisseur_name,
            FireEffectTag = ensure.quoted(f"weapon_effet_tag{self.index}"),
            NbProj=1,
            WeaponIndex=self.weapon_index,
            WeaponShootDataPropertyName=[ensure.quoted(f'WeaponShootData_0_{self.index}')]
        )