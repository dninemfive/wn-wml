# - If enum,
#       assert that input value is in generated type (or aliases)
#       if alias, resolve to simplified value
#       resolve simplified value to original value
#       no need to resolve quotations or anything since original is stored
from typing import Callable

from warno_mfw.utils.ndf import ensure


def _enum_resolver(s: str, enum_name: str, aliases: dict[str, str], originals: dict[str, str]) -> str:
    assert s in aliases or s in originals or s in originals.values(), f'{s} is not a valid value for enumerated type {enum_name}! Must be one of: (values)'
    if s in aliases:
        s = aliases[s]
    if s in originals:
        s = originals[s]
    return s

# - If not enum,
#       no assertion required
#       make sure prefix and/or quotation applied to input value
def _formatter(s: str, name: str, prefix: str = "", quotes: bool = False):
    s = ensure.prefix(ensure.unquoted(s), prefix)
    if quotes:
        s = ensure.quoted(s)
    return s

Resolver = Callable[[str, str, dict[str, str], dict[str, str]], str]
ResolverType = Literal['enum', 'format']

def _resolve_resolver(resolver: ResolverType | Resolver) -> Resolver:
    if isinstance(resolver, Resolver):
        return resolver
    elif resolver == 'enum':
        return _enum_resolver
    elif resolver == 'format':
        return _formatter

from ....hints import *

def _validate_PylonSet(s: str, values: dict[str, str], aliases: dict[str, str] | None = None) -> str:
    pass