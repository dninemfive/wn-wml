from typing import Iterable, Self, SupportsIndex

from utils.ndf import ensure
from ndf_parse.model import List, ListRow, Map, MapRow
from ndf_parse.model.abc import CellValue


class MapWrapper(object):
    def __init__(self: Self, map: Map):
        self._map = map

    def __iter__(self: Self) -> Iterable[tuple[str, CellValue]]:
        yield from [(row.key, row.value) for row in self._map]

    def __getitem__(self: Self, key: str) -> CellValue:
        return self._map.by_key(key).value
    
    def __setitem__(self: Self, key: str, value: CellValue) -> None:
        if key in self.keys:
            self.replace(key, value)
        else:
            self.add(key, value)

    def __contains__(self: Self, key: str) -> bool:
        return key in self.keys

    @property
    def keys(self: Self) -> Iterable[str]:
        yield from [row.key for row in self._map]

    @property
    def values(self: Self) -> Iterable[str]:
        yield from [row.value for row in self._map]

    def add(self: Self, key: str, val: str) -> None:
        self._map.add(ensure.maprow(key, val))

    def remove(self: Self, key: str) -> None:
        self._map.remove_by_key(key)

    def replace(self: Self, key: str, value: CellValue) -> None:
        self._map.by_key(key).value = ensure.ndf_type(value)