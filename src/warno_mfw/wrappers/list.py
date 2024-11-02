from typing import Callable, Generic, Iterable, Self, SupportsIndex, TypeVar

from ndf_parse.model import List, ListRow
from ndf_parse.model.abc import CellValue
from warno_mfw.utils.ndf import ensure

T = TypeVar('T')

class ListWrapper(Generic[T]):
    def __init__(self: Self,
                 list: List,
                 from_ndf: Callable[[CellValue], T] | None = None,
                 to_ndf: Callable[[T], CellValue] | None = None):
        self._list = list
        self._from_ndf = from_ndf if from_ndf is not None else T.__init__
        self._to_ndf = to_ndf if to_ndf is not None else ensure.ndf_type

    def __iter__(self: Self) -> Iterable[T]:
        yield from [x.value for x in self._list]

    def __getitem__(self: Self, index: int) -> T:
        return self._from_ndf(self._list[index])

    # TODO: adder for ListRows themselves
    def add(self: Self, val: CellValue) -> None:
        self._list.add(ensure.listrow(self._to_ndf(val)))

    def remove(self: Self, val: T) -> None:
        self._list.remove(self._list.find_by_cond(lambda x: x.value == self._to_ndf(val)))