from curses import wrapper
from typing import Any, Callable, Self, Type

import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
import utils.ndf.unit_module as modules
# from context.mod_creation import ModCreationContext
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue
from wrappers.unit_modules.tags import TagsModuleWrapper
from wrappers.unit_modules.type_unit import TypeUnitModuleWrapper

from wrappers.unit_modules._abc import UnitModuleWrapper, UnitModuleKey


class UnitWrapper(object):
    # ctx: ModCreationContext
    def __init__(self: Self, ctx, object: Object):
        self.ctx = ctx
        self.object = object
        self._cached_module_wrappers: dict[UnitModuleKey, UnitModuleWrapper] = {}

    def _get_wrapper(self: Self, wrapper_type: Type[UnitModuleWrapper]):
        if wrapper_type._module_key not in self._cached_module_wrappers:
            type, name = wrapper_type._module_key
            type_or_name = type if name is None else name
            by_name: bool = name is not None
            self._cached_module_wrappers[wrapper_type._module_key] = wrapper_type(self.ctx, self.get_module(type_or_name, by_name))
        return self._cached_module_wrappers[wrapper_type._module_key]

    @property
    def tags(self: Self) -> TagsModuleWrapper:
        return self._get_wrapper(TagsModuleWrapper)
    
    @property
    def unit_type(self: Self) -> TypeUnitModuleWrapper:
        return self._get_wrapper(TypeUnitModuleWrapper)

    # modules
    
    def append_module(self: Self, module: Object | ListRow):
        return modules.append(self.object, module)
    
    def append_module_from(self: Self, other_unit: Object, type_or_name: str, by_name: bool = False):
        return modules.append_from(self.object, other_unit, type_or_name, by_name)
    
    def edit_module_members(self: Self, module: str, by_name: bool = False, **changes: CellValue | None):
        edit.members(self.get_module(module, by_name), **changes)
    
    def get_module(self: Self, type_or_name: str, by_name: bool = False) -> Object:
        return modules.get(self.object, type_or_name, by_name)
    
    def get_module_index(self: Self, type_or_name: str, by_name: bool = False) -> int:
        return modules.get_index(self.object, type_or_name, by_name)
    
    def get_module_row(self: Self, type_or_name: str, by_name: bool = False) -> ListRow:
        return modules.get_row(self.object, type_or_name, by_name)
    
    def replace_module(self: Self, type_or_name: str, module: CellValue, by_name: bool = False):
        return modules.replace_module(self.object, module, type_or_name, by_name)
    
    def replace_module_from(self: Self, other_unit: str | Object, type_or_name: str, by_name: bool = False) -> None:
        if isinstance(other_unit, str):
            other_unit = self.ctx.get_unit(ensure.unit_descriptor(other_unit))
        return modules.replace_from(self.object, other_unit, type_or_name, by_name)    
    
    def remove_module(self: Self, type_or_name: str, by_name: bool = False):
        return modules.remove(self.object, type_or_name, by_name)
    
    def remove_module_where(self: Self, predicate: Callable[[ListRow], bool]):
        return modules.remove_where(self.object, predicate)