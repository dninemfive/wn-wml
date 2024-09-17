from ndf_parse.model import MemberRow, Object
from ndf_parse.model.abc import CellValue
import utils.ndf.ensure as ensure

def member(obj: Object, name: str, value: CellValue):
    value = ensure.ndf_type(value)
    try:
        index = obj.by_member(name).index
        obj[index].value = value
    except:
        obj.add(MemberRow(value, name))

def members(obj: Object, **kwargs: CellValue):
    for k, v in kwargs.items():
        member(obj, k, v)