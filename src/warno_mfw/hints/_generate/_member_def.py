from typing import Callable, Iterable, Self

from ndf_parse.model import MemberRow, Object, List

from warno_mfw.utils.ndf import ensure

MEMBER_LEN = 40
LITERAL_INDENT = "".rjust(MEMBER_LEN + len('= Literal['))

class MemberDef(object):
    def __init__(self: Self, member_name: str, prefix: str | None = None, special_formatter: Callable[[Self], str] | None = None, aliases: dict[str | Iterable[str]] | None = None):
        self.member_name = member_name
        self.prefix = prefix
        self.values: set[str] = set()
        self.special_formatter = special_formatter
        self.aliases = aliases

    def add(self: Self, row: MemberRow) -> None:
        value = row.value
        if isinstance(value, str):
            self.values.add(ensure.no_prefix(ensure.unquoted(value), self.prefix))
        elif isinstance(value, List):
            for item in value:
                self.values.add(ensure.no_prefix(ensure.unquoted(item.value), self.prefix))

    def literal_lines(self: Self) -> Iterable[str]:
        if self.special_formatter is not None:
            yield from self.special_formatter(self)
        else:
            yield from _default_formatter(self)
    
def _base_formatter(name: str, values: Iterable[str]) -> str:
    items = [ensure.quoted(x) for x in sorted(values)]
    return f'{name.ljust(MEMBER_LEN)}= Literal[{f',\n{LITERAL_INDENT}'.join(items)}]'

def _default_formatter(member_def: MemberDef) -> Iterable[str]:
    yield _base_formatter(member_def.member_name, member_def.values)
    if member_def.aliases is not None and any(member_def.aliases):
        yield _base_formatter(f'{member_def.member_name}Alias', member_def.aliases.values())

def _specialties_list_formatter(member_def: MemberDef) -> Iterable[str]:
    primaries, secondaries = [], []
    for item in member_def.values:
        (secondaries if item.startswith('_') else primaries).append(item)
    yield _base_formatter('PrimarySpecialty',   primaries)
    yield _base_formatter('SecondarySpecialty', [ensure.no_prefix(x, '_') for x in secondaries])