from typing import Self

import ensure

class Validator(object):
    """
    General class for ensuring that certain string arguments in the ndf are valid. For example:
    - Ensures membership in an enum for types which can't be added to
    - Ensures proper formatting, e.g. wrapping something in quotes or placing a prefix 
    """
    def __init__(self: Self, prefix: str, suffix: str, *values: str):
        self.prefix = prefix
        self.suffix = suffix
        self.values = values

    def ensure_valid(self: Self, s: str) -> str:
        s = ensure.prefix_and_suffix(s, self.prefix, self.suffix)
        assert s in self.values, f'{s} is not one of the valid values: {str(self.values)}'
        return s