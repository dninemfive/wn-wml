from __future__ import annotations

from abc import ABC
from ast import TypeVar
from typing import Any, Self, Type

import context.mod_creation
import utils.ndf.edit as edit
from ndf_parse.model import Object
from ndf_parse.model.abc import CellValue

class NdfObjectWrapper(ABC):
    def __init__(self: Self, ctx: context.mod_creation.ModCreationContext, obj: Object):
        self.ctx = ctx
        self.object = obj

    def _get(self: Self, member: str) -> CellValue:
        return self.object.by_member(member).value
    
    def _set(self: Self, member: str, value: CellValue | None) -> None:
        edit.member(self.object, member, value)