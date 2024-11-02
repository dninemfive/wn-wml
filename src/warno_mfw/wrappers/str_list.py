from typing import Callable, Iterable, Self, SupportsIndex

from warno_mfw.utils.ndf import ensure
from ndf_parse.model import List, ListRow

StrNormalizer = Callable[[str], str]

class StrListWrapper(object):
    def __init__(self: Self, list: List, callbacks: tuple[StrNormalizer, StrNormalizer]= (lambda x: x, lambda x: x)):
        self._list = list
        self._pre_add, self._post_get = callbacks

    def __iter__(self: Self) -> Iterable[str]:
        yield from [x.value for x in self._list]

    def __getitem__(self: Self, index: int) -> str:
        return self._post_get(self._list[index])

    def add(self: Self, val: str) -> None:
        self._list.add(ensure.listrow(self._pre_add(val)))

    def remove(self: Self, val: str) -> None:
        # print(f'{val} -> {self._pre_add(val)}')
        self._list.remove(self._list.find_by_cond(lambda x: x.value == self._pre_add(val)))

    def replace(self: Self, to_replace: str, value: str) -> None:
        index: int = self._list.find_by_cond(lambda x: x.value == to_replace)
        self._list.replace(index, self._pre_add(value))