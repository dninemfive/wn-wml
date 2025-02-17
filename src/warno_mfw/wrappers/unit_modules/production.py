from numbers import Number
from typing import Self

import warno_mfw.utils.ndf.edit as edit
import warno_mfw.utils.ndf.ensure as ensure
from warno_mfw.wrappers.map import MapWrapper
from ndf_parse.model import List, Object
from warno_mfw import hints
from warno_mfw.hints._validation import _resolve_Factory

from ._abc import UnitModuleKey, UnitModuleWrapper

COMMAND_POINTS_KEY = '$/GFX/Resources/Resource_CommandPoints'

class ProductionModuleWrapper(UnitModuleWrapper):
    _module_key = UnitModuleKey('TProductionModuleDescriptor')
    @property
    def Factory(self: Self) -> str:
        return self.object.by_member('Factory').value
    
    @Factory.setter
    def Factory(self: Self, value: hints.FactoryOrAlias) -> None:
        edit.members(self.object, Factory=_resolve_Factory(value))

    @property
    def ProductionTime(self: Self) -> int:
        return int(self.object.by_member('ProductionTime').value)
    
    @ProductionTime.setter
    def ProductionTime(self: Self, value: int) -> None:
        edit.members(ProductionTime=value)

    @property
    def ProductionRessourcesNeeded(self: Self) -> MapWrapper:
        if not hasattr(self, '_production_ressources_needed'):
            self._production_ressources_needed = MapWrapper(self.object.by_member('ProductionRessourcesNeeded').value)
        return self._production_ressources_needed
    
    @property
    def command_point_cost(self: Self) -> int:
        return int(self.ProductionRessourcesNeeded[COMMAND_POINTS_KEY])
    
    @command_point_cost.setter
    def command_point_cost(self: Self, value: int) -> None:
        self.ProductionRessourcesNeeded[COMMAND_POINTS_KEY] = value