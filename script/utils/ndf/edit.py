from ndf_parse.model import MemberRow, Object
from ndf_parse.model.abc import CellValue

def member(obj: Object, name: str, value: CellValue | None):
    try:
        index = obj.by_member(name).index
        obj[index].value = value
    except:
        obj.add(MemberRow(value, name))

def members(obj: Object, **kwargs: CellValue | None):
    for k, v in kwargs.items():
        member(obj, k, v)