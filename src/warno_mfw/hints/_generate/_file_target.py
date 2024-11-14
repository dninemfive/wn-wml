from typing import Callable, Iterable, Self

from ndf_parse import Mod
from ndf_parse.model import List, ListRow, MemberRow, Object
from ndf_parse.model.abc import CellValue

from warno_mfw.hints import paths

from ...utils.types.message import Message, try_nest
from ._member_def import MemberDef


def _default_selector(row: ListRow) -> Iterable[Object]:
    yield row.value

class FileTarget(object):
    def __init__(self: Self, file_path: str, selector: Callable[[ListRow], Iterable[ListRow]] | None = None, **targets: list[MemberDef]):
        self.file_path = file_path
        self.selector = selector if selector is not None else _default_selector
        self.targets = targets

    def add(self: Self, row: ListRow, msg: Message) -> None:
        with msg.nest(row.namespace) as _:
            for object in self.selector(row):
                if not isinstance(object, Object):
                    continue
                if object.type in self.targets:
                    for member_def in self.targets[object.type]:
                        try:
                            member_def.add(object.by_member(member_def.member_name))
                        except:
                            pass

    def add_all(self: Self, mod: Mod, msg: Message | None = None):
        with try_nest(msg, self.file_path) as msg:
            with mod.edit(self.file_path, save=False) as file:
                for row in file:
                    self.add(row, msg)

    def to_lines(self: Self, line_selector: Callable[[MemberDef], str]) -> Iterable[str]:
        for v in self.targets.values():
            for m in sorted(v, key=lambda x: x.member_name):
                yield line_selector(m)

