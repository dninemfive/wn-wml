from typing import Callable, Self
from warno_mfw.utils.ndf import ensure

Validator = Callable[[str], str]

_require_quotes: Validator = ensure.quoted

def _require_prefix(prefix: str) -> Validator:
    return lambda x: ensure.prefix(x, prefix)

def _require_membership(*valid_values: str) -> Validator:
    def validator(s: str) -> str:
        assert s in valid_values, f'{s} is not one of the valid values: {str(sorted(valid_values))}'
        return s
    return validator
    
