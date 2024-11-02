from dataclasses import dataclass
from typing import Self

from ndf_parse.model import Object
import warno_mfw.utils.ndf.ensure as ensure

@dataclass
class TDepictionDescriptor(object):
    SelectorId: list[str]
    MeshDescriptor: str

    @staticmethod
    def from_ndf(ndf: Object) -> Self:
        assert ndf.type == 'TDepictionDescriptor', f"Can't parse TDepictionDescriptor from object of type {ndf.type}!"
        return TDepictionDescriptor([x for x in ndf.by_member('SelectorId').value], ndf.by_member('MeshDescriptor').value)
    
    def to_ndf(self: Self) -> Object:
        return ensure._object('TDepictionDescriptor', SelectorId=self.SelectorId, MeshDescriptor=self.MeshDescriptor)