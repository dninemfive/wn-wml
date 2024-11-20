from typing import Callable, Iterable, Self

from .._constants._base_formatter import _base_formatter, MEMBER_LEN
from ndf_parse.model import List, MemberRow

from warno_mfw.utils.ndf import ensure


class MemberDef(object):
    def __init__(self:              Self,
                 member_name:       str,
                 prefix:            str | None = None,
                 special_formatter: Callable[[Self], str] | None = None,
                 aliases:           dict[str | Iterable[str]] | None = None):
        self.member_name = member_name
        self.prefix = prefix
        self.values: dict[str, str] = {}
        self.special_formatter = special_formatter
        self.aliases = {v: k for k, v in aliases.items()} if aliases is not None else None
        self.needs_quotes: bool | None = None

    @property
    def has_aliases(self: Self) -> bool:
        return self.aliases is not None and any(self.aliases)

    @property
    def alias_name(self: Self) -> str:
        assert self.has_aliases, 'Attempted to access `alias_name` on MemberDef instance with no aliases!'
        return f'{self.member_name}Alias'
    
    @property
    def member_or_alias_name(self: Self) -> str:
        assert self.has_aliases, 'Attempted to access `value_or_alias_name` on MemberDef instance with no aliases!'
        return f'{self.member_name}OrAlias'

    def _add_internal(self: Self, s: str) -> None:
        normalized: str = ensure.no_prefix(ensure.unquoted(s), self.prefix)
        self.values[normalized] = s

    def add(self: Self, row: MemberRow) -> None:
        value = row.value
        needs_quotes = value.startswith('"') or value.startswith("'")
        if self.needs_quotes is None:
            self.needs_quotes = needs_quotes
        elif not (self.needs_quotes == needs_quotes):
            print(f'Inconsistent quotation requirements in member {self.member_name}!')
        
        if isinstance(value, str):
            self._add_internal(value)
        elif isinstance(value, List):
            for item in value:
                self._add_internal(item.value)

    def literal_lines(self: Self) -> Iterable[str]:
        if self.special_formatter is not None:
            print("special formatter:", self.special_formatter.__name__)
            yield from self.special_formatter(self)
        else:
            yield from _default_formatter(self)

    def enum_lines(self: Self) -> Iterable[str]:
        if self.has_aliases:
            yield repr(self.aliases)
        yield repr(self.values)
    
def _default_formatter(member_def: MemberDef) -> Iterable[str]:
    yield _base_formatter(member_def.member_name, member_def.values)
    if member_def.has_aliases:
        yield _base_formatter(f'{member_def.alias_name}', member_def.aliases)
        yield f'{f'{member_def.member_or_alias_name}'.ljust(MEMBER_LEN)}= {member_def.member_name} | {member_def.alias_name}'
