from __future__ import annotations

from abc import ABC
from typing import Any, Callable, Self, Type

import warno_mfw.context.mod_creation as ctx
import warno_mfw.utils.ndf.edit as edit
from ndf_parse.model import List, Object
from ndf_parse.model.abc import CellValue
import warno_mfw.utils.ndf.unit_module as modules


class UnitModuleKey(tuple):
    # https://stackoverflow.com/a/13094796
    def __new__(cls: Type, type: str, name: str | None = None):
        return super(UnitModuleKey, cls).__new__(cls, (type, name))
    
    @property
    def type(self: Self) -> str:
        return self[0]

    @property
    def name(self: Self) -> str | None:
        return self[1]

    @property
    def by_name(self: Self) -> bool:
        return self.name is not None
    
    @property
    def type_or_name(self: Self) -> str:
        return self.name if self.name is not None else self.type

ModuleGetMethod = Callable[[modules.UnitOrModules, UnitModuleKey], Object]

def _default_get_method(unit_or_modules: modules.UnitOrModules, key: UnitModuleKey) -> Object:
    result = modules.get(unit_or_modules, key.type_or_name, key.by_name)
    return result

def get_t_module_selector(unit_or_modules: modules.UnitOrModules, key: UnitModuleKey) -> Object:
    return modules.get_selector(unit_or_modules, key.type)

class UnitModuleWrapper(ABC):
    _module_key: UnitModuleKey      = None
    _get_method: ModuleGetMethod    = _default_get_method
    
    def __init__(self: Self, ctx: ctx.ModCreationContext, modules: List):
        self.ctx = ctx
        self.object = self.__class__._get_method(modules, self._module_key)

    def edit_members(self: Self, **changes: CellValue) -> None:
        for k, v in changes.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                edit.member(self.object, k, v)

    def copy(self: Self, to_copy: Object | Self) -> None:
        assert isinstance(to_copy, (Object, UnitModuleWrapper)), f'{self.__class__.__name__}.copy() argument 1 must be Object or Self, not {to_copy.__class__.__name__}!'
        if not isinstance(to_copy, Object):
            to_copy = to_copy.object
        self.object = to_copy.copy()