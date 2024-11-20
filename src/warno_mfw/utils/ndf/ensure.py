from numbers import Number
from typing import Callable
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object, Template
from ndf_parse.model.abc import CellValue

def NdfListRow(val: CellValue | ListRow) -> ListRow:
    if isinstance(val, ListRow):
        return val
    else:
        return ListRow(value=val)
    
def NdfMapRow(pair_or_key: tuple[str, CellValue] | MapRow | str, value_or_none: CellValue | None = None):
    if isinstance(pair_or_key, str):
        if value_or_none is None:
            raise ValueError("If first argument is not a tuple or MapRow, second argument must not be None!")
        # print(value_or_none)
        return MapRow(pair_or_key, ndf_type(value_or_none))
    elif isinstance(pair_or_key, MapRow):
        return pair_or_key
    else:
        return MapRow(pair_or_key[0], ndf_type(pair_or_key[1]))
    
def NdfMemberRow(pair_or_key: tuple[str, CellValue] | MemberRow | str, value_or_none: CellValue | None = None):
    if isinstance(pair_or_key, str):
        if value_or_none is None:
            raise ValueError("If first argument is not a tuple or MemberRow, second argument must not be None!")
        return MemberRow(member=pair_or_key, value=ndf_type(value_or_none))
    elif isinstance(pair_or_key, MemberRow):
        return pair_or_key
    else:
        return MemberRow(member=pair_or_key[0], value=ndf_type(pair_or_key[1]))
    
def NotNdfRow(row_or_value: ListRow | MemberRow | MapRow) -> CellValue:
    if isinstance(row_or_value, (ListRow, MemberRow, MapRow)):
        return row_or_value.value
    return row_or_value

def _add_from(map_or_object: Map | Object, items: dict[str, CellValue | None] | list[tuple[str, CellValue | None]]):
    row_fn = NdfMapRow if isinstance(map_or_object, Map) else NdfMemberRow
    row_type = MapRow if isinstance(map_or_object, Map) else MemberRow
    for item in (items.items() if isinstance(items, dict) else items):
        if isinstance(item, row_type):
            map_or_object.add(item)
        else:
            k, v = item
            if v is None:
                continue
            map_or_object.add(row_fn(str(k), v))

def NdfMap(_dict: Map | dict = {}, *kvps: tuple[str, CellValue | None], **items: CellValue | None) -> Map:
    if isinstance(_dict, Map):
        return _dict
    result = Map()
    _add_from(result, _dict)
    _add_from(result, kvps)
    _add_from(result, items)
    return result

def NdfObject(type: str, _dict: Object | dict = {}, *kvps: tuple[str, CellValue], **items: CellValue) -> Object:
    result = Object(type)
    _add_from(result, _dict)
    _add_from(result, kvps)
    _add_from(result, items)
    return result

def NdfTemplate(type: str, _dict: Object | dict = {}, *kvps: tuple[str, CellValue], **items: CellValue) -> Template:
    result = Template(type)
    _add_from(result, _dict)
    _add_from(result, kvps)
    _add_from(result, items)
    return result

def NdfList(_list: List | list[CellValue] = [], *items: CellValue) -> List:
    if isinstance(_list, List):
        return _list
    result = List()
    if isinstance(_list, list):
        for item in _list:
            if item is not None:
                result.add(NdfListRow(ndf_type(item)))
    else:
        result.add(NdfListRow(ndf_type(_list)))
    for item in items:
        result.add(NdfListRow(ndf_type(item)))
    return result

def ndf_type(value: dict | list | int | str, _type: str | None = None) -> Map | List | str | Object:
    if isinstance(value, dict):
        if _type is None:
            return NdfMap(value)
        else:
            return NdfObject(_type, value)
    elif isinstance(value, list):
        return NdfList(value)
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

_AffixPredicate = Callable[[str, str], bool]
_Affixer        = Callable[[str, str], str]  

def _affix_base(base:               str,
                affix:              str,
                should_apply:       _AffixPredicate,
                target_result:      bool,
                apply:              _Affixer,
                caller_name:        str) -> str:
    assert base is not None, f'Argument `base` to ensure.{caller_name}() must not be None!'
    return apply(base, affix) if should_apply(base, affix) == target_result else base 

def prefix(base: str, prefix: str) -> str:
    return _affix_base(base, prefix,
                       str.startswith, False,
                       lambda b, p: f'{p}{b}',
                       'prefix')

def suffix(base: str, suffix: str | None = None) -> str:
    return _affix_base(base, suffix,
                       str.endswith, False,
                       lambda x, y: f'{x}{y}',
                       'suffix')

def prefix_and_suffix(s: str, _prefix: str, _suffix: str) -> str:
    return prefix(suffix(s, _suffix), _prefix)

def no_prefix(base: str, prefix: str | None) -> str:
    return _affix_base(base, prefix,
                       str.startswith, True,
                       lambda b, p: b[len(p):],
                       'no_prefix')

def no_suffix(base: str, suffix: str | None) -> str:
    return _affix_base(base, suffix,
                       str.startswith, True,
                       lambda b, p: b[:-len(p)],
                       'no_suffix')

def no_prefix_or_suffix(s: str, _prefix: str, _suffix: str) -> str:
    return no_prefix(no_suffix(s, _suffix), _prefix)

def unit_descriptor(name_or_descriptor: str, showroom: bool = False) -> str:
    _prefix = 'Descriptor_Unit_' if not showroom else 'Descriptor_ShowRoomUnit_'
    return prefix(name_or_descriptor, _prefix)

def unit_path(descriptor_or_path: str) -> str:
    return prefix(descriptor_or_path, "$/GFX/Unit/")

def quoted(s: str, quote: str = "'") -> str:
    return f'{quote}{unquoted(s)}{quote}'

def unquoted(s: str | None, *quotes: str) -> str | None:
    if s is None:
        return None
    if not any(quotes):
        quotes = ["'", '"']
    for quote in quotes:
        if s.startswith(quote):
            s = s[len(quote):]
        if s.endswith(quote):
            s = s[:-len(quote)]
    return s

def quotedness_equals(s: str, should_be_quoted: bool) -> str:
    return quoted(s) if should_be_quoted else unquoted(s)

def all(list: list[str] | List, f: Callable[[str], str]) -> list[str]:
    if isinstance(list, List):
        list = [x.value for x in list]
    return [f(x) for x in list]

def guid(id: str) -> str:
    return prefix_and_suffix(id, 'GUID:{', '}')