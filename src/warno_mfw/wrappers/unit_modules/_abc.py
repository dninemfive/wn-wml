from __future__ import annotations

from abc import ABC
from typing import Any, Self, Type

import warno_mfw.context.mod_creation as ctx
import warno_mfw.utils.ndf.edit as edit
from ndf_parse.model import Object
from ndf_parse.model.abc import CellValue


class UnitModuleKey(tuple):
    # https://stackoverflow.com/a/13094796
    def __new__(cls: Type, type: str, name: str | None = None):
        return super(UnitModuleKey, cls).__new__(cls, (type, name))

class UnitModuleWrapper(ABC):
    _module_key: UnitModuleKey = None
    def __init__(self: Self, ctx: ctx.ModCreationContext, obj: Object):
        self.ctx = ctx
        self.object = obj

    def edit_members(self: Self, **changes: CellValue) -> None:
        for k, v in changes.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                edit.member(self.object, k, v)

    def copy(self: Self, to_copy: Object | Self) -> None:
        if not isinstance(to_copy, Object):
            to_copy = to_copy.object
        self.object = to_copy.copy()