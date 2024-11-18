from typing import Iterable

from warno_mfw.utils.ndf import ensure


MEMBER_LEN = 40
LITERAL_INDENT = "".rjust(MEMBER_LEN + len('= Literal['))

def _base_formatter(name: str, values: Iterable[str]) -> str:
    items = [ensure.quoted(x) for x in sorted(values)]
    return f'{name.ljust(MEMBER_LEN)}= Literal[{f',\n{LITERAL_INDENT}'.join(items)}]'