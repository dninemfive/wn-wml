import warno_mfw.utils.ndf.ensure as ensure
from ndf_parse.model import MemberRow, Object
from ndf_parse.model.abc import CellValue


def member(obj: Object, name: str, value: CellValue | None):
    if value is None:
        try:
            obj.remove_by_member(name)
        except:
            pass
    else:
        value = ensure.ndf_type(value)
        try:
            index = obj.by_member(name).index
            obj[index].value = value
        except:
            obj.add(MemberRow(value, name))

def members(obj: Object, **kwargs: CellValue | None):
    for k, v in kwargs.items():
        member(obj, k, v)