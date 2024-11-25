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

class FalseFlagOperation(BaseTraitOperation):
    def add(self: Self, unit: UnitWrapper):
        unit.modules.remove('TDangerousnessModuleDescriptor')

    # cannot remove, since we don't know the Menace the unit would have otherwise
    # might want to have a way to remove it with an argument, i suppose

class ModifyHealthOperation(BaseTraitOperation):
    def __init__(self: Self, health_on_add: int):
        self.hp_modifier = health_on_add

    def add(self: Self, unit: UnitWrapper):
        unit.modules.base_damage.MaxPhysicalDamages += self.hp_modifier

    def remove(self: Self, unit: UnitWrapper):
        unit.modules.base_damage.MaxPhysicalDamages -= self.hp_modifier

# Airborne: can add and remove. deployment distance is a fixed value for recon and non-recon units each, which should be generated from source; i think it's further for SOF units?
# Amphibious: need to get the movement types to make sure that there's a mapping between amphibious and non-amphibious ones
#             pathfind types would also be helpful
# SF:   i believe the main change is the ExperienceLevelsPackDescriptor_XP_pack_SF_v2 XP descriptor vs the normal, and also the noSIGINT tag
# transport1 and 2: i believe the primary difference between these is the TransportableTagSet, being ["Crew"] for 1 and ["Unite_transportable"] for 2
# TODO: find correlations between traits and tags in the uniteinfo module