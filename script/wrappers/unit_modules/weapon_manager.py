from typing import Self

import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
from ndf_parse.model import List, Object
from wrappers.str_list import StrListWrapper

from ._abc import UnitModuleKey, UnitModuleWrapper

class WeaponManagerModuleWrapper(UnitModuleWrapper):
    _module_key = UnitModuleKey('TModuleSelector', 'WeaponManager')

    @property
    def Default(self: Self) -> int:
        return self.object.by_member('Default').value
    @Default.setter
    def Default(self: Self, value: str):
        edit.members(self.object, Default=ensure.prefix(value, '$/GFX/Weapon/WeaponDescriptor_'))
    # Selection is always NilDescriptorIfCadavre