from dataclasses import dataclass
from typing import Self
from ndf_parse.model import Object

def _0(n: int) -> str:
    return f'_{str(n).rjust(2, '0')}'

@dataclass
class TTransportedInfantryEntry(object):
    Count: int
    Identifier: str
    Meshes: list[str]
    UniqueCount: int

    @staticmethod
    def from_ndf(ndf: Object) -> Self:
        return TTransportedInfantryEntry(
            int(ndf.by_member('Count')),
            ndf.by_member('Identifier'),
            ndf.by_member('Meshes'),
            int(ndf.by_member('UniqueCount'))
        )