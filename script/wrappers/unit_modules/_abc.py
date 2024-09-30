from abc import ABC

UnitModuleKey = tuple[str, str | None]

class UnitModuleWrapper(ABC):
    _module_key: UnitModuleKey = None

def unit_module(type: str, name: str | None = None):
    def decorate(c: UnitModuleWrapper) -> UnitModuleWrapper:
        c._module_key = (type, name)
    return decorate