from typing import Iterable

from warno_mfw.utils.ndf import ensure


MEMBER_LEN = 40
LITERAL_INDENT = "".rjust(MEMBER_LEN + len('= Literal['))

def _items(values: dict[str, str] | Iterable[str]) -> Iterable[str]:
    if isinstance(values, dict):
        for k, v in values.items():
            yield f'{ensure.quoted(k)}, # {v}'
    else:
        for item in values:
            yield f'{ensure.quoted(item)},'

def _base_formatter(name: str, values: dict[str, str] | Iterable[str]) -> str:
    return f'{name.ljust(MEMBER_LEN)}= Literal[{f'\n{LITERAL_INDENT}'.join(_items(values))}\n{LITERAL_INDENT}]'