from abc import ABC, abstractmethod
from typing import Self

from ndf_parse.model import List, Object
import warno_mfw.utils.ndf.ensure as ensure
from warno_mfw.wrappers.unit import UnitWrapper
from warno_mfw.hints import SecondarySpecialty
from warno_mfw.hints._validation import _resolve_SecondarySpecialty

class BaseTraitOperation(ABC):        
    def _can(self: Self, op: str) -> bool:
        return hasattr(self, op) and callable(getattr(self, op))

    @property
    def can_add(self: Self) -> bool:
        return self._can('add')
    
    @property
    def can_remove(self: Self) -> bool:
        return self._can('remove')

class CapaciteOperation(BaseTraitOperation):
    def __init__(self: Self, *capacites: str):
        self.capacites = [ensure.prefix(x, '$/GFX/EffectCapacity/Capacite_') for x in capacites]
        
    def add(self: Self, unit: UnitWrapper):
        if unit.modules.capacites is None:
            unit.modules.capacites = self.capacites
        else:
            unit.modules.capacites.add(*self.capacites)

    def remove(self: Self, unit: UnitWrapper):
        # if capacites *is* None, nothing to remove from and no reason to add an empty module
        if unit.modules.capacites is not None:
            unit.modules.capacites.remove(*self.capacites)