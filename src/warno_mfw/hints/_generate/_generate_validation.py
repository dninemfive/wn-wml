from typing import Callable, Self
from warno_mfw.utils.ndf import ensure

Validator = Callable[[str], str]

require_quotes: Validator = ensure.quoted

def require_prefix(prefix: str) -> Validator:
    return lambda x: ensure.prefix(x, prefix)

def require_membership(*valid_values: str) -> Validator:
    def validator(s: str) -> str:
        assert s in valid_values, f'{s} is not one of the valid values: {str(sorted(valid_values))}'
        return s
    return validator

class ValidationSet(object):
    def __init__(self: Self, *validators: Validator):
        self.validators = validators

    def validate(self: Self, s: str) -> str:
        for validator in self.validators:
            s = validator(s)
        return s
    
def StandardValidationSet(require_quotes: bool, prefix: str | None = None, *valid_values: str) -> ValidationSet:
    validators: list[Validator] = []
    if require_quotes:
        validators.append(require_quotes)
    if prefix is not None:
        validators.append(require_prefix(prefix))
    if any(valid_values):
        validators.append(require_membership(*valid_values))
    return ValidationSet(*validators)

# if enum, ensure that it resolves to one of the enumerated values
# ensure that quotation remains the same as in source (either all or none quoted)
#   print warning if source is inconsistent
# ensure prefix
# need custom handling for specialties