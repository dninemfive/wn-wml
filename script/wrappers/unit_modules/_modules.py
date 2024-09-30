from typing import Callable, Iterable, Self, SupportsIndex, Type

import utils.ndf.unit_module as modules
import utils.ndf.edit as edit
from ndf_parse.model import List, ListRow, Object
from ndf_parse.model.abc import CellValue
from utils.ndf import ensure

from script.wrappers.unit_modules.tags import TagsModuleWrapper
from script.wrappers.unit_modules.type_unit import TypeUnitModuleWrapper
from script.wrappers.unit_modules.unit_ui import UnitUiModuleWrapper

from ._abc import UnitModuleKey, UnitModuleWrapper


class UnitModulesWrapper(object):
    def __init__(self: Self, ndf: List):
        self._ndf = ndf
        self._cached_module_wrappers: dict[UnitModuleKey, UnitModuleWrapper] = {}

    def __iter__(self: Self) -> Iterable[CellValue]:
        yield from [x.value for x in self._ndf]

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
    def type(self: Self) -> TypeUnitModuleWrapper:
        return self._get_wrapper(TypeUnitModuleWrapper)
    
    @property
    def ui(self: Self) -> UnitUiModuleWrapper:
        return self._get_wrapper(UnitUiModuleWrapper)

    # modules
    
    def append(self: Self, module: str | Object | ListRow):
        return modules.append(self._ndf, module)
    
    def append_module_from(self: Self, other_unit: Object, type_or_name: str, by_name: bool = False):
        return modules.append_from(self._ndf, other_unit, type_or_name, by_name)
    
    def edit_members(self: Self, module: str, by_name: bool = False, **changes: CellValue | None):
        edit.members(self.get_module(module, by_name), **changes)
    
    def get_module(self: Self, type_or_name: str, by_name: bool = False) -> Object:
        return modules.get(self._ndf, type_or_name, by_name)
    
    def get_module_index(self: Self, type_or_name: str, by_name: bool = False) -> int:
        return modules.get_index(self._ndf, type_or_name, by_name)
    
    def get_module_row(self: Self, type_or_name: str, by_name: bool = False) -> ListRow:
        return modules.get_row(self._ndf, type_or_name, by_name)
    
    def replace_module(self: Self, type_or_name: str, module: CellValue, by_name: bool = False):
        return modules.replace(self._ndf, module, type_or_name, by_name)
    
    def replace_module_from(self: Self, other_unit: str | Object, type_or_name: str, by_name: bool = False) -> None:
        if isinstance(other_unit, str):
            other_unit = self.ctx.get_unit(ensure.unit_descriptor(other_unit))
        return modules.replace_from(self._ndf, other_unit, type_or_name, by_name)
    
    def remove_module(self: Self, type_or_name: str, by_name: bool = False):
        return modules.remove(self._ndf, type_or_name, by_name)
    
    def remove_module_where(self: Self, predicate: Callable[[ListRow], bool]):
        return modules.remove_where(self._ndf, predicate)