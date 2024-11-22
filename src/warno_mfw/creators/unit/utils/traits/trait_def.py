from abc import ABC, abstractmethod
from typing import Self

from ndf_parse.model import List, Object
from .trait_operation import BaseTraitOperation
import warno_mfw.utils.ndf.ensure as ensure
from warno_mfw.wrappers.unit import UnitWrapper
from warno_mfw.hints import SecondarySpecialty
from warno_mfw.hints._validation import _resolve_SecondarySpecialty

class TraitDef(object):
    def __init__(self: Self, specialty: SecondarySpecialty | str, *operations: BaseTraitOperation):
        self.specialty = _resolve_SecondarySpecialty(specialty)
        self.operations = operations

    @property
    def _can(self: Self, op: str) -> bool:
        return all(x._can(op) for x in self.operations)

    @property
    def can_add(self: Self) -> bool:
        return self._can('add')
    
    @property
    def can_remove(self: Self) -> bool:
        return self._can('remove')
    
    def _apply(self: Self, op: str, unit: UnitWrapper) -> None:
        if not self._can(op):
            raise Exception(f"Cannot perform operation '{op}' with a specialty of {self.specialty} to an arbitrary unit!")
        for operation in self.operations:
            getattr(operation, op)(unit)
    
    def add(self: Self, unit: UnitWrapper) -> None:
        return self._apply('add', unit)
    
    def remove(self: Self, unit: UnitWrapper) -> None:
        return self._apply('remove', unit)