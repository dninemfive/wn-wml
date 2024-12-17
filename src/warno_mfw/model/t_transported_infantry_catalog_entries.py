from dataclasses import dataclass
from typing import Self

from warno_mfw.utils.ndf import ensure
from .t_transported_infantry_entry import TTransportedInfantryEntry
from ndf_parse.model import Object

@dataclass
class TTransportedInfantryCatalogEntries(object):
    Catalog: str
    Entries: list[TTransportedInfantryEntry]

    def __getitem__(self: Self, identifier: str) -> TTransportedInfantryEntry | None:
        for entry in self.Entries:
            if ensure.unquoted(entry.Identifier) == ensure.unquoted(identifier):
                return entry
        return None

    @staticmethod
    def from_ndf(ndf: Object) -> Self:
        ...