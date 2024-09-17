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

def ensure_listrow(val: CellValue | ListRow) -> ListRow:
    if isinstance(val, ListRow):
        return val
    else:
        return ListRow(value=val)



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