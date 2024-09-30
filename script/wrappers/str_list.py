from typing import Iterable, Self, SupportsIndex

from ndf_parse.model import List, ListRow

from script.utils.ndf import ensure

class StrListWrapper(object):
    def __init__(self: Self, list: List):
        self._list = list

    def __iter__(self: Self) -> Iterable[str]:
        yield from [x.value for x in self._list]

    def add(self: Self, val: str) -> None:
        self._list.add(ensure.listrow(val))

    def remove(self: Self, val: str) -> None:
        self._list.remove(self._list.find_by_cond(lambda x: x.value == val))

    def replace(self: Self, to_replace: str, value: str) -> None:
        index: int = self._list.find_by_cond(lambda x: x.value == to_replace)
        self._list.replace(index, value)