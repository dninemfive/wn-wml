from typing import Self

import warno_mfw.utils.ndf.edit as edit
import warno_mfw.utils.ndf.ensure as ensure
from ndf_parse.model import List, Object

from ._abc import UnitModuleKey, UnitModuleWrapper

class WeaponManagerModuleWrapper(UnitModuleWrapper):
    _module_key = UnitModuleKey('TModuleSelector', 'WeaponManager')

    @property
    def Default(self: Self) -> int:
        return self.object.by_member('Default').value
    @Default.setter
    def Default(self: Self, value: str):
        edit.members(self.object, Default=ensure.prefix(value, '$/GFX/Weapon/WeaponDescriptor_'))

    @staticmethod
    def new() -> Object:
        return ensure._object(
            'TModuleSelector',
            Default='(not initialized)',
            Selection=['~/NilDescriptorIfCadavre']
        )