from typing import Self

import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
from wrappers.str_list import StrListWrapper
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