from typing import Self

import warno_mfw.utils.ndf.ensure as ensure
from ndf_parse.model import Object

from ._abc import WeaponDepictionOperator


class DepictionOperator_WeaponInstantFire(WeaponDepictionOperator):
    def to_ndf(self: Self) -> Object:
        return ensure._object(
            'DepictionOperator_WeaponInstantFire',
            Anchors=self.anchors,
            FireEffectTag = ensure.quoted(f"weapon_effet_tag{self.index}"),
            NbProj=self.count,
            WeaponShootDataPropertyName=[ensure.quoted(f'WeaponShootData_{i}_{self.index}') for i in range(self.count)]
        )