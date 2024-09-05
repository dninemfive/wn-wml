# https://realpython.com/primer-on-python-decorators/#fancy-decorators
from functools import wraps
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, Object
from ndf_parse.model.abc import CellValue
from typing import Any, Generator
from message import Message, try_nest

def edit_member(obj: Object, name: str, value: CellValue | None):
    index = obj.by_member(name).index
    obj[index].value = value

def edit_members(obj: Object, **kwargs: CellValue | None):
    for k, v in kwargs.items():
        edit_member(obj, k, v)

def dict_to_map(input: dict) -> Map:
    result = Map()
    for k, v in input.items():
        result.add(MapRow((k, str(v))))
    return result

def object_has_type(object: Object, type: str) -> bool:
    try:
        return object.type == type
    except:
        return False
    
def replace_by_type(list: List, type: str, value: CellValue):
    index: int = list.find_by_cond(lambda x: object_has_type(x.value, type))
    list.replace(index, value)

def get_unit_module(unit_list: List, unit_name: str, module_type: str) -> ListRow | None:
    unit_object: Object = unit_list.by_namespace(f'Descriptor_Unit_{unit_name}').value
    modules: List = unit_object.by_member('ModulesDescriptors').value
    return modules.find_by_cond(lambda x: object_has_type(x.value, module_type))

def replace_unit_module(unit: Object, module_type: str, module: ListRow | Object):
    modules: List = unit.by_member('ModulesDescriptors').value
    replace_by_type(modules, module_type, ensure_listrow(module))

def replace_unit_modules(unit: Object, **kwargs: ListRow | Object):
    for k, v in kwargs.items():
        replace_unit_module(unit, k, v)

def editing_or_reading(save: bool):
    return 'Editing' if save else 'Reading'

def edit_or_read_file_with_msg(mod: Mod, msg: Message, path: str, padding: int = 0, save: bool = True) -> Mod:
    with msg.nest(f'{editing_or_reading(save)} {path}', padding) as _:
        return mod.edit(path, save)
    
def ensure_listrow(val: CellValue | ListRow) -> ListRow:
    if isinstance(val, ListRow):
        return val
    else:
        return ListRow(value=val)
    
def root_paths(base_path: str, *paths: str) -> Generator:
    for p in paths:
        yield f'{base_path}\\{p}.ndf'

def ndf_path(path: str, save: bool = True):
    """
    Decorator which allows defining NDF edits to a particular file:

    @ndf_path("Divisions.ndf")
    """
    def decorate(f: callable[List, Message]):
        # @wraps doesn't understand self (afaict) so using it here is counterproductive
        def wrap(self: Any, mod: Mod, msg: Message | None, *args: Any, **kwargs: Any):
            with try_nest(msg, f"{editing_or_reading(save)} {path}") as new_msg:
                with mod.edit(path, save) as data:
                    return f(self, data, new_msg, *args, **kwargs)
        return wrap
    return decorate