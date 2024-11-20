# - If enum,
#       assert that input value is in generated type (or aliases)
#       if alias, resolve to simplified value
#       resolve simplified value to original value
#       no need to resolve quotations or anything since original is stored
from typing import Callable

from warno_mfw.utils.ndf import ensure

def _values(aliases: dict[str, str], originals: dict[str, str]) -> str:
    result_set = set()
    for key in aliases.keys():
        result_set.add(key)
    for k, v in originals.items():
        result_set.add(k)
        result_set.add(v)
    return '\n\t'.join(sorted(result_set))

def _enum_resolver(s: str, enum_name: str, aliases: dict[str, str], originals: dict[str, str]) -> str:
    if aliases is None:
        aliases = {}
    assert ((s in aliases 
             or s in originals 
             or s in originals.values()),
             f'{s} is not a valid value for enumerated type {enum_name}! Must be one of:\n\t{_values(aliases, originals)}')
    if s in aliases:
        s = aliases[s]
    if s in originals:
        s = originals[s]
    return s

# - If not enum,
#       no assertion required
#       make sure prefix and/or quotation applied to input value
def _format_resolver(s: str, prefix: str = "", quotes: bool = False):
    s = ensure.prefix(ensure.unquoted(s), prefix)
    if quotes:
        s = ensure.quoted(s)
    return s

Resolver = Callable[[str, str, dict[str, str], dict[str, str]], str]
