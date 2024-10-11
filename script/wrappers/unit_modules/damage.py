from typing import Self

import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
from ndf_parse.model import List, Object
from wrappers.str_list import StrListWrapper

from ._abc import UnitModuleWrapper
from ._decorator import unit_module


@unit_module('TBaseDamageModuleDescriptor')
class BaseDamageModuleWrapper(UnitModuleWrapper):
    @property
    def MaxPhysicalDamages(self: Self) -> int:
        return int(self.object.by_member('MaxPhysicalDamages').value)
    @MaxPhysicalDamages.setter
    def MaxPhysicalDamages(self: Self, value: int):
        edit.members(self.object, MaxPhysicalDamages=value)
    # TODO: remaining stuff