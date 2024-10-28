from enum import member
from numbers import Number
from typing import Callable, Iterable, Literal, Type
from typing import get_args as literal_values
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object, Template
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
        # print(value_or_none)
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
            map_or_object.add(row_fn(str(k), v))

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

def _template(type: str, _dict: Object | dict = {}, *kvps: tuple[str, CellValue], **items: CellValue) -> Object:
    result = Template(type)
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
            if item is not None:
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
    elif isinstance(value, tuple) and len(value) == 2:
        return (ndf_type(value[0]), ndf_type(value[1]))
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

def unit_descriptor(name_or_descriptor: str, showroom: bool = False) -> str:
    _prefix = 'Descriptor_Unit_' if not showroom else 'Descriptor_ShowRoomUnit_'
    return prefix(name_or_descriptor, _prefix)

def unit_path(descriptor_or_path: str) -> str:
    return prefix(descriptor_or_path, "$/GFX/Unit/")

def quoted(s: str, quote: str = "'") -> str:
    return prefix_and_suffix(s, quote, quote)

def unquoted(s: str, *quotes: str) -> str:
    if not any(quotes):
        quotes = ["'", '"']
    for quote in quotes:
        if s.startswith(quote):
            s = s[len(quote):]
        if s.endswith(quote):
            s = s[:-len(quote)]
    return s

def suffix(s: str, suffix: str) -> str:
    return s if s.endswith(suffix) else f'{s}{suffix}'

def prefix_and_suffix(s: str, _prefix: str, _suffix: str) -> str:
    return prefix(suffix(s, _suffix), _prefix)

def no_prefix(s: str, prefix: str) -> str:
    if s.startswith(prefix):
        return s[len(prefix):]
    return s

def no_suffix(s: str, suffix: str) -> str:
    if s.endswith(suffix):
        return s[:-len(suffix)]
    return s

def no_prefix_or_suffix(s: str, _prefix: str, _suffix: str) -> str:
    return no_prefix(no_suffix(s, _suffix), _prefix)

# type: Literal[str]
def _including_unquoted(*literal_types) -> list[str]:
    result: set[str] = set()
    for literal_type in literal_types:
        for s in literal_values(literal_type.__value__):
            # https://discuss.python.org/t/get-origin-get-args-typealiastype/56254/3 :thonk:
            result.add(s)
            result.add(unquoted(s, "'"))
    return sorted(result)

def literal(s: str, *literal_types):
    valid_values = _including_unquoted(*literal_types)
    assert s in valid_values, f"{s} is not one of {valid_values}"
    return quoted(s, "'")

def all(list: list[str] | List, f: Callable[[str], str]) -> list[str]:
    if isinstance(list, List):
        list = [x.value for x in list]
    return [f(x) for x in list]

def guid(id: str) -> str:
    return prefix_and_suffix(id, 'GUID:{', '}')