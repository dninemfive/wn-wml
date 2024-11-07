from typing import Callable, Iterable, Self

from ndf_parse.model import List, ListRow, Object
from ndf_parse.model.abc import Row, CellValue

from ._member_def import MemberDef


class EnumGenerator(object):
    def __init__(self: Self, selector: Callable[[ListRow], Iterable[CellValue]] | None = None, **targets: list[MemberDef]):
        self.targets = targets
        self.selector = selector if selector is not None else lambda x: x

    def add(self: Self, row: ListRow) -> str:
        for item in self.selector(row):
        # for module_row in item.value.by_member('ModulesDescriptors').value:
            if isinstance(item, Object) and item.type in self.targets:
                for member_def in self.targets[item.type]:
                    member_def.add(item.by_member(member_def.member_name))