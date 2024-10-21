from typing import Self

import mw2.utils.ndf.edit as edit
import mw2.utils.ndf.ensure as ensure
from mw2.wrappers.str_list import StrListWrapper
from ndf_parse.model import List, Object

from ._abc import UnitModuleKey, UnitModuleWrapper


class BaseDamageModuleWrapper(UnitModuleWrapper):
    _module_key = UnitModuleKey('TBaseDamageModuleDescriptor')
    @property
    def MaxPhysicalDamages(self: Self) -> int:
        return int(self.object.by_member('MaxPhysicalDamages').value)
    @MaxPhysicalDamages.setter
    def MaxPhysicalDamages(self: Self, value: int):
        edit.members(self.object, MaxPhysicalDamages=value)
    # TODO: remaining stuff