from typing import Self

from warno_mfw.context.mod_creation import ModCreationContext
from warno_mfw.utils.ndf import ensure
from ndf_parse.model import Object, MemberRow
from ndf_parse.model.abc import CellValue

def unwrap(ndf: Object) -> dict[str, CellValue]:
    result: dict[str, CellValue] = {}
    for member in ndf:
        result[member.member] = member.value
    return result

class NdfFirstOrderObject(object):
    def __init__(self: Self, ctx: ModCreationContext, obj: Object):
        self.ctx = ctx
        self.obj = obj

class NdfDescriptor(NdfFirstOrderObject):
    @property
    def DescriptorId(self: Self) -> str:
        return ensure.not_guid(self.obj.by_member('DescriptorId'))
    
    @DescriptorId.setter
    def DescriptorId(self: Self, value: str) -> str:
        self.obj.by_member('DescriptorId').value = ensure.guid(value)