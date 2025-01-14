from typing import Literal, Self

import warno_mfw.utils.ndf.ensure as ensure
from ndf_parse.model import List, Object
from warno_mfw import hints

from ._abc import UnitModuleKey, UnitModuleWrapper


class TypeUnitModuleWrapper(UnitModuleWrapper):
    _module_key = UnitModuleKey('TTypeUnitModuleDescriptor')
    def __init__(self: Self, ctx, obj: Object):
        self.ctx = ctx
        self.object = obj
        
    @property
    def Coalition(self: Self) -> str:
        return self.object.by_member('Coalition').value
    
    @Coalition.setter
    def Coalition(self: Self, value: hints.CoalitionOrAlias) -> None:
        # TODO: enum aliases.
        if value == 'NATO':
            value = 'Allied'
        if value == 'PACT':
            value = 'Axis'
        self.object.by_member('Coalition').value = ensure.prefix(value, 'ECoalition/')

    @property
    def MotherCountry(self: Self) -> str:
        return self.object.by_member('MotherCountry').value
    
    @MotherCountry.setter
    def MotherCountry(self: Self, val: hints.MotherCountry | str) -> None:
        self.object.by_member('MotherCountry').value = ensure.quoted(val)

    @property
    def AcknowUnitType(self: Self) -> str:
        return self.object.by_member('AcknowUnitType').value
    
    @AcknowUnitType.setter
    def AcknowUnitType(self: Self, val: hints.AcknowUnitType | str) -> None:
        self.object.by_member('AcknowUnitType').value = ensure.prefix(val, '~/TAcknowUnitType_')

    @property
    def TypeUnitFormation(self: Self) -> str:
        return self.object.by_member('TypeUnitFormation').value
    
    @TypeUnitFormation.setter
    def TypeUnitFormation(self: Self, val: hints.TypeUnitFormation | str) -> None:
        self.object.by_member('TypeUnitFormation').value = ensure.quoted(val)