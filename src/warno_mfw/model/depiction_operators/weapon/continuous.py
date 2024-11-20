from typing import Self

import warno_mfw.utils.ndf.ensure as ensure
from ndf_parse.model import Object

from ._abc import WeaponDepictionOperator


class DepictionOperator_WeaponContinuousFire(WeaponDepictionOperator):
    def to_ndf(self: Self) -> Object:
        return ensure.NdfObject(
            'DepictionOperator_WeaponContinuousFire',
            Anchors=self.anchors,
            FireEffectTag = ensure.quoted(f"weapon_effet_tag{self.index}"),
            NbFX=self.count,
            WeaponActiveAndCanShootPropertyName=ensure.quoted(f'WeaponActiveAndCanShoot_{self.index}'),
            WeaponShootDataPropertyName=ensure.quoted(f'WeaponShootData_0_{self.index}')
        )