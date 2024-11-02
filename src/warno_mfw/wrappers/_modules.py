from __future__ import annotations

from typing import Callable, Iterable, Self, SupportsIndex, Type, TypeVar

import context.mod_creation as ctx
import utils.ndf.edit as edit
import utils.ndf.unit_module as modules
import wrappers.unit as uw
from utils.ndf import ensure
from ndf_parse.model import List, ListRow, Object
from ndf_parse.model.abc import CellValue

from .unit_modules._abc import UnitModuleKey, UnitModuleWrapper
from .unit_modules.damage import BaseDamageModuleWrapper
from .unit_modules.production import ProductionModuleWrapper
from .unit_modules.tags import TagsModuleWrapper
from .unit_modules.type_unit import TypeUnitModuleWrapper
from .unit_modules.unit_ui import UnitUiModuleWrapper
from .unit_modules.weapon_manager import WeaponManagerModuleWrapper

UnitRef = str | Object | object # wrappers.unit.UnitWrapper
ModuleRef = str | tuple[str, bool]

T = TypeVar('T', covariant=True, bound=UnitModuleWrapper)

class UnitModulesWrapper(object):
    def __init__(self: Self, ctx: ctx.ModCreationContext, modules_ndf: List):
        self.ctx = ctx
        self._modules_ndf = modules_ndf
        self._cached_module_wrappers: dict[UnitModuleKey, UnitModuleWrapper] = {}

    def __iter__(self: Self) -> Iterable[CellValue]:
        yield from [x.value for x in self._modules_ndf]

    def _get_wrapper(self: Self, wrapper_type: Type[T]) -> T:
        if wrapper_type._module_key not in self._cached_module_wrappers:
            type, name = wrapper_type._module_key
            type_or_name = type if name is None else name
            by_name: bool = name is not None
            self._cached_module_wrappers[wrapper_type._module_key] = wrapper_type(self.ctx, self.get(type_or_name, by_name))
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
    
    @property
    def production(self: Self) -> ProductionModuleWrapper:
        return self._get_wrapper(ProductionModuleWrapper)
    
    @property
    def base_damage(self: Self) -> BaseDamageModuleWrapper:
        return self._get_wrapper(BaseDamageModuleWrapper)
    
    @property
    def weapon_manager(self: Self) -> WeaponManagerModuleWrapper | None:
        try:
            return self._get_wrapper(WeaponManagerModuleWrapper)
        except:
            return None
        
    @weapon_manager.setter
    def weapon_manager(self: Self, value: str | None) -> None:
        manager = self.weapon_manager
        if value is None and manager is not None:
            del self._cached_module_wrappers[WeaponManagerModuleWrapper._module_key]
        elif isinstance(value, str):
            if manager is not None:
                manager.Default = value
            else:
                self._modules_ndf.add(ListRow(WeaponManagerModuleWrapper.new(), namespace='WeaponManager'))
                self.weapon_manager.Default = value

    # modules

    def _deref(self: Self, unit_ref: UnitRef) -> Object:
        if isinstance(unit_ref, str):
            return self.ctx.get_unit(ensure.unit_descriptor(unit_ref)).object
        elif isinstance(unit_ref, uw.UnitWrapper):
            return unit_ref.object
        return unit_ref
    
    def append(self: Self, module: str | Object | ListRow):
        return modules.append(self._modules_ndf, module)
    
    def append_from(self: Self, other_unit: UnitRef, type_or_name: str, by_name: bool = False):
        return modules.append_from(self._modules_ndf, self._deref(other_unit), type_or_name, by_name)
    
    def edit_members(self: Self, module: str, by_name: bool = False, **changes: CellValue | None):
        edit.members(self.get(module, by_name), **changes)

    def try_edit_members(self: Self, module: str, by_name: bool = False, **changes: CellValue | None):
        try:
            self.edit_members(module, by_name, **changes)
        except:
            pass
    
    def get(self: Self, type_or_name: str, by_name: bool = False) -> Object:
        return modules.get(self._modules_ndf, type_or_name, by_name)
    
    def get_index(self: Self, type_or_name: str, by_name: bool = False) -> int:
        return modules.get_index(self._modules_ndf, type_or_name, by_name)
    
    def get_row(self: Self, type_or_name: str, by_name: bool = False) -> ListRow:
        return modules.get_row(self._modules_ndf, type_or_name, by_name)
    
    def replace(self: Self, type_or_name: str, module: CellValue, by_name: bool = False):
        return modules.replace(self._modules_ndf, module, type_or_name, by_name)
    
    def replace_from(self: Self, other_unit: UnitRef, type_or_name: str, by_name: bool = False) -> None:
        return modules.replace_from(self._modules_ndf, self._deref(other_unit), type_or_name, by_name)
    
    def replace_from_many(self: Self, other_unit: UnitRef, *modules: ModuleRef) -> None:
        # dereferencing here avoids duplicate work in each replace_from call
        other_unit = self._deref(other_unit)
        for module in modules:
            if isinstance(module, str):
                module = (module, False)
            type_or_name, by_name = module
            self.replace_from(other_unit, type_or_name, by_name)
    
    def remove(self: Self, type_or_name: str, by_name: bool = False):
        return modules.remove(self._modules_ndf, type_or_name, by_name)
    
    def remove_where(self: Self, predicate: Callable[[ListRow], bool]):
        return modules.remove_where(self._modules_ndf, predicate)