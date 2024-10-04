from abc import ABC
from typing import Self

import utils.ndf.edit as edit
from ndf_parse.model import Object
from ndf_parse.model.abc import CellValue

UnitModuleKey = tuple[str, str | None]

class UnitModuleWrapper(ABC):
    _module_key: UnitModuleKey = None

def unit_module(type: str, name: str | None = None):
    def decorate(c: UnitModuleWrapper) -> UnitModuleWrapper:
        c._module_key = (type, name)
    return decorate

def edit_members(self: Self, **changes: CellValue) -> None:
    for k, v in changes:
        if hasattr(self, k):
            setattr(self, k, v)
        else:
            edit.member(self.object, k, v)