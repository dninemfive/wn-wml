from typing import Callable, Literal
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue
from warno_mfw.utils.ndf import ensure

MODULES_DESCRIPTORS = "ModulesDescriptors"
T_MODULE_SELECTOR = "TModuleSelector"
_GetMode = Literal['by type', 'by name', 'by default']

def get_modules_descriptors(unit_or_modules: Object | List) -> List:
    if isinstance(unit_or_modules, List):
        return unit_or_modules
    return unit_or_modules.by_member(MODULES_DESCRIPTORS).value

def _get_row_by_name(modules: List, name: str) -> ListRow:
    return modules.by_name(name)

def _get_row_by_type(modules: List, type: str) -> ListRow | None:
    for module in modules.match_pattern(f'{type}()'):
        return module
    return None

def _get_row_by_selector_default_type(modules: List, type: str) -> ListRow | None:
    for module in modules.match_pattern(f'{T_MODULE_SELECTOR}()'):
        try:
            if module.value.by_member('Default').type == type:
                return module
        except:
            continue
    return None

_GET_MODES: dict[_GetMode, Callable[[List, str], ListRow | None]] = {
    'by type': _get_row_by_type,
    'by name': _get_row_by_name,
    'by default': _get_row_by_selector_default_type
}

def get_row(unit_or_modules: Object | List, type_or_name: str, mode: _GetMode) -> ListRow:
    result: ListRow | None = None
    modules = get_modules_descriptors(unit_or_modules)
    if mode in _GET_MODES:
        result = _GET_MODES[mode](modules, type_or_name)
    else:
        raise Exception(f'Unrecognized modules.get_row mode: {mode}!')
    if result is None:
        report = f"Could not find module {type_or_name} {mode} on "
        report += f"unit {unit_or_modules.by_member('ClassNameForDebug').value}" if isinstance(unit_or_modules, Object) else f'list {str(unit_or_modules[:32])}'
        raise KeyError(report)
    return result

def get_selector(unit_or_modules: Object | List, default_type: str, selector_type: str = 'TModuleSelector') -> ListRow:
    for module in get_modules_descriptors(unit_or_modules).match_pattern(f'{selector_type}()'):
        try:
            default: Object = module.value
            if default.type == default_type:
                return module
        except:
            continue
    raise Exception(f'Could not find {selector_type} with Default.type == {default_type}!')

def get_index(unit_or_modules: Object | List, type_or_name: str, mode: _GetMode = 'by type') -> int:
    return get_row(unit_or_modules, type_or_name, mode).index

def get(unit_or_object: Object | List, type_or_name: str, mode: _GetMode = 'by type') -> Object:
    return get_row(unit_or_object, type_or_name, mode).value

def replace(unit_or_modules: Object | List, value: CellValue, type_or_name: str, by_name: bool = False) -> None:
    get_row(unit_or_modules, type_or_name, by_name).value = value

def replace_where(unit_or_modules: Object | List, value: CellValue, predicate: Callable[[ListRow], bool]) -> None:
    get_modules_descriptors(unit_or_modules).find_by_cond(predicate).value = value

def replace_from(dest_unit_or_modules: Object | List, src_unit: Object, type_or_name: str, by_name: bool = False):
    replace(dest_unit_or_modules, get(src_unit, type_or_name, by_name).copy(), type_or_name, by_name)

def append(dest_unit_or_modules: Object | List, module: ListRow | Object):
    get_modules_descriptors(dest_unit_or_modules).add(ensure.NdfListRow(module))

def append_from(dest_unit_or_list: Object | List, src_unit: Object, type_or_name: str, by_name: bool = False):
    append(dest_unit_or_list, get_row(src_unit, type_or_name, by_name))

def remove(target_unit_or_list: Object, type_or_name: str, by_name: bool = False):
    get_modules_descriptors(target_unit_or_list).remove(get_index(target_unit_or_list, type_or_name, by_name))

def remove_where(target_unit_or_list: Object, predicate: Callable[[ListRow], bool]):
    modules: List = get_modules_descriptors(target_unit_or_list)
    modules.remove(modules.find_by_cond(predicate).index)

def _path(parent_name: str,
          module_path: str,
          remaining_path: list[str]) -> str:
    result = f'{parent_name}{module_path}'
    if any(remaining_path):
        result += f'/{'/'.join(remaining_path)}'
    return result

def path_by_type(parent_name: str, module_name: str, *remaining_path: str) -> str:
    return _path(parent_name, f':{ensure.no_prefix_or_suffix(module_name, 'T', "ModuleDescriptor")}', remaining_path)

def path_by_name(parent_name: str, module_name: str, *remaining_path: str) -> str:
    return _path(parent_name, f'[{module_name}]', remaining_path)