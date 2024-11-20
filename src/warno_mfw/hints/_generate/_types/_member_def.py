from typing import Any, Callable, Iterable, Literal, Self

from .._constants._base_code_generators import _base_literal_generator, MEMBER_LEN, _enum_resolver_generator, _format_resolver_generator
from ndf_parse.model import List, MemberRow

from warno_mfw.utils.ndf import ensure

class MemberDef(object):
    def __init__(self:                  Self,
                 member_name:           str,
                 prefix:                str | None = None,
                 enum:                  bool = True,
                 literal_generator:     Callable[[Self], Iterable[str]] | None = None,
                 resolver_generator:    Callable[[Self], Iterable[str]] | None = None,                 
                 aliases:               dict[str | Iterable[str]] | None = None):
        self.member_name = member_name
        self.prefix = prefix
        self.values: dict[str, str] = {}
        self.literal_generator = literal_generator if literal_generator is not None else _default_literal_generator
        self.resolver_generator = (resolver_generator
                                   if resolver_generator is not None
                                   else (_enum_resolver_generator_wrapper
                                         if enum
                                         else _format_resolver_generator_wrapper))
        self.aliases = {v: k for k, v in aliases.items()} if aliases is not None else None
        self.type = type

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
    
    @property
    def raw_values(self: Self) -> Iterable[str]:
        yield from self.values.values()

    @property
    def needs_quotes(self: Self) -> bool:
        result: bool | None = None
        for value in self.raw_values:
            has_quotes = value.startswith('"') or value.startswith("'")
            if result is None:
                result = has_quotes
            elif result != has_quotes:
                print(f'Inconsistent quotation requirements in member {self.member_name}!')
                return False
        return result

    def _add_internal(self: Self, s: str) -> None:
        normalized: str = ensure.no_prefix(ensure.unquoted(s), self.prefix)
        self.values[normalized] = s

    def add(self: Self, row: MemberRow) -> None:
        value = row.value
        if isinstance(value, str):
            self._add_internal(value)
        elif isinstance(value, List):
            for item in value:
                self._add_internal(item.value)

    def literal_lines(self: Self) -> Iterable[str]:
        yield from self.literal_generator(self)

    def resolver_lines(self: Self) -> Iterable[str]:
        yield from self.resolver_generator(self)
    
def _default_literal_generator(member_def: MemberDef) -> Iterable[str]:
    yield _base_literal_generator(member_def.member_name, member_def.values)
    if member_def.has_aliases:
        yield _base_literal_generator(f'{member_def.alias_name}', member_def.aliases)
        yield f'{f'{member_def.member_or_alias_name}'.ljust(MEMBER_LEN)}= {member_def.member_name} | {member_def.alias_name}'

def _format_resolver_generator_wrapper(member_def: MemberDef) -> Iterable[str]:
    yield _format_resolver_generator(member_def.member_name, member_def.prefix, member_def.needs_quotes)

def _enum_resolver_generator_wrapper(member_def: MemberDef) -> Iterable[str]:
    yield _enum_resolver_generator(member_def.member_name, member_def.aliases, member_def.values)