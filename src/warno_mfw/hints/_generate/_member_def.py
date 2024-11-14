from typing import Self

from ndf_parse.model import MemberRow, Object, List

from warno_mfw.utils.ndf import ensure

MEMBER_LEN = 40
LITERAL_INDENT = "".rjust(MEMBER_LEN + len('= Literal['))

class MemberDef(object):
    def __init__(self: Self, member_name: str, prefix: str | None = None):
        self.member_name = member_name
        self.prefix = prefix
        self.values: set[str] = set()

    def add(self: Self, row: MemberRow) -> None:
        value = row.value
        if isinstance(value, Object):
            self.values.add(ensure.no_prefix(ensure.unquoted(value), self.prefix))
        elif isinstance(value, List):
            for item in value:
                self.values.add(ensure.no_prefix(ensure.unquoted(item), self.prefix))

    def literal_line(self: Self) -> str:
        items = [ensure.quoted(x) for x in sorted(self.values)]
        return f'{self.member_name.ljust(MEMBER_LEN)}= Literal[{f',\n{LITERAL_INDENT}'.join(items)}]'