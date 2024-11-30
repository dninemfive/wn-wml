from __future__ import annotations

from typing import TYPE_CHECKING, Self

from warno_mfw.hints import SecondarySpecialty
from warno_mfw.hints._validation import _resolve_SecondarySpecialty

from .trait_operation import BaseTraitOperation

if TYPE_CHECKING:
    from warno_mfw.wrappers.unit import UnitWrapper

_ADD = 'add_to'
_REMOVE = 'remove_from'

class TraitDef(object):
    def __init__(self: Self, specialty: SecondarySpecialty | str, *operations: BaseTraitOperation):
        self.specialty = _resolve_SecondarySpecialty(specialty)
        self.operations = operations

    def _can(self: Self, op: str) -> bool:
        return all(x._can(op) for x in self.operations)

    @property
    def can_add(self: Self) -> bool:
        return self._can(_ADD)
    
    @property
    def can_remove(self: Self) -> bool:
        return self._can(_REMOVE)
    
    def _apply(self: Self, op: str, unit: UnitWrapper) -> None:
        if not self._can(op):
            raise Exception(f"Cannot perform operation '{op}' with a specialty of {self.specialty} to an arbitrary unit!")
        for operation in self.operations:
            getattr(operation, op)(unit)
    
    def add_to(self: Self, unit: UnitWrapper) -> None:
        # avoid duplicating traits
        if self.specialty in unit.modules.ui.SpecialtiesList:
            return
        self._apply(_ADD, unit)
        unit.modules.ui.SpecialtiesList.add(self.specialty)
    
    def remove_from(self: Self, unit: UnitWrapper) -> None:
        if self.specialty not in unit.modules.ui.SpecialtiesList:
            return
        self._apply(_REMOVE, unit)
        unit.modules.ui.SpecialtiesList.remove(self.specialty)