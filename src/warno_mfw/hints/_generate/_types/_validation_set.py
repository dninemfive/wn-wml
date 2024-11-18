from typing import Self
from .._constants._validators import Validator, _require_quotes, _require_prefix, _require_membership

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
        validators.append(_require_quotes)
    if prefix is not None:
        validators.append(_require_prefix(prefix))
    if any(valid_values):
        validators.append(_require_membership(*valid_values))
    return ValidationSet(*validators)