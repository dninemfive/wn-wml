from typing import TypeVar

T = TypeVar['T']

def module_type(s: str):
    def decorate(c: T) -> T:
        c._module_type = s
    return decorate