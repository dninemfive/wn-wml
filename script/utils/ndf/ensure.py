from enum import member
from numbers import Number
from typing import Type
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue

def listrow(val: CellValue | ListRow) -> ListRow:
    if isinstance(val, ListRow):
        return val
    else:
        return ListRow(value=val)
    
def maprow(pair_or_key: tuple[str, CellValue] | MapRow | str, value_or_none: CellValue | None = None):
    if isinstance(pair_or_key, str):
        if value_or_none is None:
            raise ValueError("If first argument is not a tuple or MapRow, second argument must not be None!")
        return MapRow(k=pair_or_key, v=ndf_type(value_or_none))
    elif isinstance(pair_or_key, MapRow):
        return pair_or_key
    else:
        return MapRow(k=pair_or_key[0], v=ndf_type(pair_or_key[1]))
    
def memberrow(pair_or_key: tuple[str, CellValue] | MemberRow | str, value_or_none: CellValue | None = None):
    if isinstance(pair_or_key, str):
        if value_or_none is None:
            raise ValueError("If first argument is not a tuple or MemberRow, second argument must not be None!")
        return MemberRow(k=pair_or_key, v=ndf_type(value_or_none))
    elif isinstance(pair_or_key, MemberRow):
        return pair_or_key
    else:
        return MemberRow(k=pair_or_key[0], v=ndf_type(pair_or_key[1]))

def map(_dict: Map | dict, *kvps: tuple[str, CellValue], **items: CellValue) -> Map:
    if isinstance(_dict, Map):
        return _dict
    result = Map()
    for k, v in _dict.items():
        result.add(maprow(k, v))
    for k, v in kvps:
        result.add(maprow(k, v))
    for k, v in items:
        result.add(maprow(k, v))
    return result

def object(type: str, _dict: Object | dict, *kvps: tuple[str, CellValue], **items: CellValue) -> Object:
    result = Object(type)
    for k, v in _dict.items():
        result.add(memberrow(k, v))
    for k, v in kvps:
        result.add(memberrow(k, v))
    for k, v in items:
        result.add(memberrow(k, v))
    return result

def list(_list: List | list[CellValue], *items: CellValue) -> List:
    if isinstance(_list, List):
        return _list
    result = List()
    for item in _list:
        result.add(listrow(item))
    for item in items:
        result.add(listrow(item))
    return result

def ndf_type(value: dict | list | int | str, type: str | None = None) -> Map | List | str | Object:
    if isinstance(value, dict):
        if type is None:
            return map(value)
        else:
            return object(type, value)
    elif isinstance(value, list):
        return list(value)
    elif isinstance(value, Number):
        return str(value)
    elif isinstance(value, str):
        return value
    raise TypeError(f"ensure.ndf_type() doesn't work on type {type(value)}!")

def unit_path(descriptor: str) -> str:
    return descriptor if descriptor.startswith("$/GFX/Unit/") else f'$/GFX/Unit/{descriptor}'

def quotes(s: str, quote: str = '"') -> str:
    if not s.startswith(quote):
        s = f'{quote}{s}'
    if not s.endswith(quote):
        s = f'{s}{quote}'
    return s