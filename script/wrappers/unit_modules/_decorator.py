from typing import TypeVar
from ._abc import UnitModuleWrapper 


T = TypeVar('T', covariant=True, bound=UnitModuleWrapper)

def unit_module(type: str, name: str | None = None):
    def decorate(c: T) -> T:
        c._module_key = (type, name)
    return decorate