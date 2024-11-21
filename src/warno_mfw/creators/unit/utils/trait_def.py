from abc import ABC, abstractmethod
from typing import Self

from ndf_parse.model import List, Object
import warno_mfw.utils.ndf.ensure as ensure
from warno_mfw.wrappers.unit import UnitWrapper
from warno_mfw.hints import SecondarySpecialty
from warno_mfw.hints._validation import _resolve_SecondarySpecialty

class BaseTraitDef(ABC):
    def __init__(self: Self, specialty: SecondarySpecialty | str):
        self.specialty = _resolve_SecondarySpecialty(specialty)

    @abstractmethod
    def add(self: Self, unit: UnitWrapper):
        ...

    @abstractmethod
    def remove(self: Self, unit: UnitWrapper):
        ...

class CapaciteTraitDef(BaseTraitDef):
    def __init__(self: Self, specialty: SecondarySpecialty, *capacites: str):
        super().__init__(specialty)
        self.capacites = [ensure.prefix(x, '$/GFX/EffectCapacity/Capacite_') for x in capacites]
        
    def add(self: Self, unit: UnitWrapper):
        if self.specialty not in unit.modules.ui.SpecialtiesList:
            unit.modules.ui.SpecialtiesList.add(self.specialty)
        for capacite in self.capacites:
            # TODO: unit capacite module wrapper
            ...