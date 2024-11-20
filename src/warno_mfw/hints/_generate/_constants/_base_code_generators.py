from typing import Iterable

from warno_mfw.utils.ndf import ensure

from ._resolvers import _enum_resolver, _format_resolver

MEMBER_LEN = 40
LITERAL_INDENT = "".rjust(MEMBER_LEN + len('= Literal['))

def _base_literal_generator(name: str, values: dict[str, str] | Iterable[str]) -> str:
    items = sorted([ensure.quoted(x) for x in (values.keys() if isinstance(values, dict) else values)])
    return f'{name.ljust(MEMBER_LEN)}= Literal[{f',\n{LITERAL_INDENT}'.join(items)}]'

def _resolve_sig_generator(name: str) -> str:
    return f'def _resolve_{name}(s: str) -> str:\n\t'

def _enum_resolver_generator(name: str, aliases: dict[str, str] | None, values: dict[str, str]) -> str:
    return f'{_resolve_sig_generator(name)}return {_enum_resolver.__name__}(s, {repr(aliases)}, {repr(values)})'

def _format_resolver_generator(name: str, prefix: str | None, require_quotes: bool) -> str:
    if prefix is None:
        prefix = ''
    return f'{_resolve_sig_generator(name)}return {_format_resolver.__name__}(s, {ensure.quoted(prefix)}, {require_quotes})'