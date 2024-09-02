from ndf_parse.model import Map, MapRow, Object
from ndf_parse.model.abc import CellValue

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