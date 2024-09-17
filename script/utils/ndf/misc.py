from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue
from typing import Any, Callable, Generator
from utils.types.message import Message, try_nest
import os
import shutil

def edit_member(obj: Object, name: str, value: CellValue | None):
    try:
        index = obj.by_member(name).index
        obj[index].value = value
    except:
        obj.add(MemberRow(value, name))

def edit_members(obj: Object, **kwargs: CellValue | None):
    for k, v in kwargs.items():
        edit_member(obj, k, v)

def dict_to_map(input: dict) -> Map:
    result = Map()
    for k, v in input.items():
        result.add(MapRow((k, str(v))))
    return result

def to_List(*input: CellValue) -> List:
    result = List()
    for s in input:
        result.add(ListRow(s))
    return result

def list_from_rows(*rows: ListRow) -> List:
    result = List()
    for row in rows:
        result.add(row)
    return result

def object_has_type(object: Object, type: str) -> bool:
    try:
        return object.type == type
    except:
        return False
    
def replace_by_type(list: List, type: str, value: CellValue):
    index: int = list.find_by_cond(lambda x: object_has_type(x.value, type))
    list.replace(index, value)

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

def load_ndf_path(path: str, save: bool = True):
    """
    Decorator which allows defining NDF edits to a particular file:

    @ndf_path("Divisions.ndf")
    """
    def decorate(f: Callable[..., None]):
        # @wraps doesn't understand self (afaict) so using it here is counterproductive
        def wrap(self: Any, mod: Mod, msg: Message | None, *args: Any, **kwargs: Any):
            with try_nest(msg, f"{editing_or_reading(save)} {path}") as _:
                with mod.edit(path, save) as data:
                    return f(self, data, *args, **kwargs)
        return wrap
    decorate._ndf_path = path
    return decorate

def ndf_path(path: str, save: bool = True):
    """
    Decorator which allows defining NDF edits to a particular file:

    @ndf_path("Divisions.ndf")
    """
    def decorate(f: Callable[..., None]):
        # @wraps doesn't understand self (afaict) so using it here is counterproductive
        def wrap(self: Any, ndf: dict[str, List], msg: Message | None, *args: Any, **kwargs: Any):
            with try_nest(msg, f"{editing_or_reading(save)} {path}") as _:
                return f(self, ndf[path], *args, **kwargs)
        return wrap
    # lost the link but this was suggested in a StackExchange post
    decorate._ndf_path = path
    return decorate

def make_obj(type: str, **props: CellValue) -> Object:
    result = Object(type)
    for k, v in props.items():
        result.add(MemberRow(value=v, member=k))
    return result

def make_map(**items: CellValue) -> Map:
    result = Map()
    for k, v in items.items():
        result.add(MapRow(k=k, v=v))

def add_image(ndf_file: List,
              src_file_path: str,
              mod_output_path: str,
              folder_relative_to_gamedata: str,
              image_name: str,
              texture_bank_name: str,
              component_state: str = "~/ComponentState/Normal") -> str:
    destination_folder = os.path.join(mod_output_path, "GameData", folder_relative_to_gamedata)
    os.makedirs(destination_folder)
    dst_image_filename = f'{image_name}{os.path.splitext(src_file_path)[1]}'
    shutil.copyfile(src_file_path, os.path.join(destination_folder, dst_image_filename))
    texture_obj = make_obj('TUIResourceTexture_Common',
                           FileName=f'"GameData:/{folder_relative_to_gamedata}/{dst_image_filename}"')
    ndf_file.add(ListRow(texture_obj, namespace=image_name))
    ndf_file.by_name(texture_bank_name).value\
            .by_member("Textures").value\
            .add(key=f'"{image_name}"',
                 value=dict_to_map({component_state:f"~/{image_name}"}))
    return f'"{image_name}"'

def map_from_tuples(*tuples: tuple[str, CellValue]) -> Map:
    result = Map()
    for k, v in tuples:
        result.add(MapRow(k=k, v=v))
    return result

def map_from_rows(*rows: MapRow) -> Map:
    result = Map()
    for row in rows:
        result.add(row)
    return result

def ensure_unit_path(descriptor: str) -> str:
    return descriptor if descriptor.startswith("$/GFX/Unit/") else f'$/GFX/Unit/{descriptor}'