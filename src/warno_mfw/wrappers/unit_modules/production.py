from numbers import Number
from typing import Self

import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
from constants.enums import Factory
import constants.enums as enums
import constants.literals as literals
from wrappers.map import MapWrapper
from ndf_parse.model import List, Object

from ._abc import UnitModuleKey, UnitModuleWrapper

COMMAND_POINTS_KEY = '$/GFX/Resources/Resource_CommandPoints'

class ProductionModuleWrapper(UnitModuleWrapper):
    _module_key = UnitModuleKey('TProductionModuleDescriptor')
    @property
    def Factory(self: Self) -> str:
        return self.object.by_member('Factory').value
    
    @Factory.setter
    def Factory(self: Self, value: literals.Factory) -> None:
        edit.members(self.object, Factory=Factory.ensure_valid(value))

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