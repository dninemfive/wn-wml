from ndf_parse.model import Object
from ndf_parse.model.abc import CellValue

def edit_member(obj: Object, name: str, value: CellValue | None):
    index = obj.by_member(name).index
    obj[index].value = value

def edit_members(obj: Object, **kwargs: CellValue | None):
    for k, v in kwargs.items():
        edit_member(obj, k, v)