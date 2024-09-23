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
        return MapRow(pair_or_key, ndf_type(value_or_none))
    elif isinstance(pair_or_key, MapRow):
        return pair_or_key
    else:
        return MapRow(pair_or_key[0], ndf_type(pair_or_key[1]))
    
def memberrow(pair_or_key: tuple[str, CellValue] | MemberRow | str, value_or_none: CellValue | None = None):
    if isinstance(pair_or_key, str):
        if value_or_none is None:
            raise ValueError("If first argument is not a tuple or MemberRow, second argument must not be None!")
        return MemberRow(member=pair_or_key, value=ndf_type(value_or_none))
    elif isinstance(pair_or_key, MemberRow):
        return pair_or_key
    else:
        return MemberRow(member=pair_or_key[0], value=ndf_type(pair_or_key[1]))
    
def notrow(row_or_value: ListRow | MemberRow | MapRow) -> CellValue:
    if isinstance(row_or_value, (ListRow, MemberRow, MapRow)):
        return row_or_value.value
    return row_or_value

def _add_from(map_or_object: Map | Object, items: dict[str, CellValue | None] | list[tuple[str, CellValue | None]]):
    row_fn = maprow if isinstance(map_or_object, Map) else memberrow
    row_type = MapRow if isinstance(map_or_object, Map) else MemberRow
    for item in (items.items() if isinstance(items, dict) else items):
        if isinstance(item, row_type):
            map_or_object.add(item)
        else:
            k, v = item
            if v is None:
                continue
            map_or_object.add(row_fn(k, v))

def _map(_dict: Map | dict = {}, *kvps: tuple[str, CellValue | None], **items: CellValue | None) -> Map:
    # TODO: remove None values from existing maps and/or add kvps, items to them
    if isinstance(_dict, Map):
        return _dict
    result = Map()
    _add_from(result, _dict)
    _add_from(result, kvps)
    _add_from(result, items)
    return result

def _object(type: str, _dict: Object | dict = {}, *kvps: tuple[str, CellValue], **items: CellValue) -> Object:
    result = Object(type)
    _add_from(result, _dict)
    _add_from(result, kvps)
    _add_from(result, items)
    return result

def _list(_list: List | list[CellValue] = [], *items: CellValue) -> List:
    if isinstance(_list, List):
        return _list
    result = List()
    if isinstance(_list, list):
        for item in _list:
            result.add(listrow(ndf_type(item)))
    else:
        result.add(listrow(ndf_type(_list)))
    for item in items:
        result.add(listrow(ndf_type(item)))
    return result

def ndf_type(value: dict | list | int | str, _type: str | None = None) -> Map | List | str | Object:
    if isinstance(value, dict):
        if _type is None:
            return _map(value)
        else:
            return _object(_type, value)
    elif isinstance(value, list):
        return _list(value)
    elif isinstance(value, Number) or isinstance(value, bool):
        return str(value)
    elif isinstance(value, str)\
        or isinstance(value, Map)\
        or isinstance(value, List)\
        or isinstance(value, Object):
        return value
    raise TypeError(f"ensure.ndf_type() doesn't work on type {type(value)}!")

def prefix(s: str, prefix: str) -> str:
    return s if s.startswith(prefix) else f'{prefix}{s}'

def unit_descriptor(name_or_descriptor: str) -> str:
    return prefix(name_or_descriptor, 'Descriptor_Unit_')

def unit_path(descriptor_or_path: str) -> str:
    return prefix(descriptor_or_path, "$/GFX/Unit/")

def quoted(s: str, quote: str = '"') -> str:
    if not s.startswith(quote):
        s = f'{quote}{s}'
    if not s.endswith(quote):
        s = f'{s}{quote}'
    return s