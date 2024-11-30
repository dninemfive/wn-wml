from typing import Callable
from ndf_parse.model import List, ListRow, Object
from ndf_parse.model.abc import CellValue
from warno_mfw.utils.ndf import ensure

MODULES_DESCRIPTORS = "ModulesDescriptors"
T_MODULE_SELECTOR = "TModuleSelector"
RowPredicate = Callable[[ListRow], bool]
UnitOrModules = Object | List

def get_modules_descriptors(unit_or_modules: UnitOrModules) -> List:
    if isinstance(unit_or_modules, List):
        return unit_or_modules
    return unit_or_modules.by_member(MODULES_DESCRIPTORS).value

def _describe(unit_or_modules: UnitOrModules) -> str:
    if isinstance(unit_or_modules, Object):
        return ('on', f"unit {unit_or_modules.by_member('ClassNameForDebug').value}")
    else:
        return ('in', f'modules list {str(unit_or_modules[:32])}')

def get_row(unit_or_modules: Object | List, type_or_name: str, by_name: bool) -> ListRow:
    result: ListRow | None = None
    modules = get_modules_descriptors(unit_or_modules)
    if by_name:
        result = modules.by_name(type_or_name)
    else:
        for module in modules.match_pattern(f'{type_or_name}()'):
            result = module
            break
    if result is None:
        report = f"Could not find module {type_or_name}{" by name" if by_name else ""} {" ".join(_describe(unit_or_modules))}"
        raise KeyError(report)
    return result

def get_row_where(unit_or_modules: UnitOrModules, predicate: RowPredicate) -> ListRow:
    return get_modules_descriptors(unit_or_modules).find_by_cond(predicate)

def _selector_predicate(type: str) -> RowPredicate:
    def result(row: ListRow) -> bool:
        try:
            return row.value.type == T_MODULE_SELECTOR and row.value.by_member('Default').type == type
        except:
            return False
    return result

def get_selector_row(unit_or_modules: UnitOrModules, type: str) -> ListRow:
    return get_row_where(unit_or_modules, _selector_predicate(type))

def get_index(unit_or_modules: UnitOrModules, type_or_name: str, by_name: bool = False) -> int:
    return get_row(unit_or_modules, type_or_name, by_name).index

def get(unit_or_modules: UnitOrModules, type_or_name: str, by_name: bool = False) -> Object:
    return get_row(unit_or_modules, type_or_name, by_name).value

def get_where(unit_or_modules: UnitOrModules, predicate: RowPredicate) -> Object:
    return get_row_where(unit_or_modules, predicate).value

def get_selector(unit_or_modules: UnitOrModules, type: str) -> Object:
    try:
        return get_selector_row(unit_or_modules, type).value
    except:
        raise KeyError(f'{_describe(unit_or_modules)[1]} does not have TModuleSelector with Default.type == {type} {_describe(unit_or_modules)}!')

def replace(unit_or_modules: Object | List, value: CellValue, type_or_name: str, by_name: bool = False) -> None:
    get_row(unit_or_modules, type_or_name, by_name).value = value

def replace_where(unit_or_modules: Object | List, value: CellValue, predicate: RowPredicate) -> None:
    get_row_where(unit_or_modules, predicate).value = value

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