from typing import Literal, Self

# from warno_mfw.hints import DivisionPowerClassification
from warno_mfw.hints import Coalition, CoalitionOrAlias
from ndf_parse.model import List, ListRow, Object, MemberRow
from ndf_parse.model.abc import CellValue
from warno_mfw.hints._validation import _resolve_Coalition
from warno_mfw.utils.ndf import ensure
from warno_mfw.wrappers.map import MapWrapper
from warno_mfw.wrappers.str_list import StrListWrapper

from ._abc import NdfDescriptor, NdfFirstOrderObject

T_DIVISION_PWR = Literal['DC_PWR1', 'DC_PWR2', 'DC_PWR3'] # TODO: generate as enum in hints
T_DIVISION_TAG = str # TODO: generate

class TDeckDivisionDescriptor(NdfDescriptor):
    @property
    def CfgName(self: Self) -> str:
        return ensure.unquoted(self.obj.by_member('CfgName').value)
    
    @CfgName.setter
    def CfgName(self: Self, value: str) -> None:
        self.obj.by_member('CfgName').value = ensure.quoted(value)

    @property
    def DivisionName(self: Self) -> str:
        return ensure.unquoted(self.obj.by_member('DivisionName').value)
    
    @DivisionName.setter
    def DivisionName(self: Self, value: str) -> None:
        self.obj.by_member('DivisionName').value = ensure.quoted(value)

    @property
    def DivisionPowerClassification(self: Self) -> T_DIVISION_PWR:
        return ensure.unquoted(self.obj.by_member('DivisionPowerClassification').value)
    
    @DivisionPowerClassification.setter
    def DivisionPowerClassification(self: Self, value: T_DIVISION_PWR) -> None:
        self.obj.by_member('DivisionPowerClassification').value = value
    # &c... i *really* need to automatically generate these, but for now i need at least one example to work on a second order model

    @property
    def Coalition(self: Self) -> Coalition:
        # TODO: generate reverse resolvers to go from `ECoalition/Allied` to `Allied` (or even `NATO`?)
        return self.obj.by_member('Coalition').value
        
    @Coalition.setter
    def Coalition(self: Self, value: CoalitionOrAlias) -> None:
        self.obj.by_member('Coalition').value = _resolve_Coalition(value)

    @property
    def DivisionTags(self: Self) -> StrListWrapper:
        return StrListWrapper(self.obj.by_member('DivisionTags').value, (ensure.quoted, ensure.unquoted))
    
    @property
    def DescriptionHintTitleToken(self: Self) -> str:
        return ensure.unquoted(self.obj.by_member('DescriptionHintTitleToken').value)
    
    @DescriptionHintTitleToken.setter
    def DescriptionHintTitleToken(self: Self, value: str) -> None:
        self.obj.by_member('DescriptionHintTitleToken').value = value

    @property
    def PackList(self: Self) -> MapWrapper:
        return MapWrapper(self.obj.by_member('PackList').value)
    
    @property
    def MaxActivationPoints(self: Self) -> int:
        return int(self.obj.by_member('MaxActivationPoints'))
    
    @MaxActivationPoints.setter
    def MaxActivationPoints(self: Self, value: int) -> None:
        self.obj.by_member('MaxActivationPoints').value = str(value)

    # ok this should be enough for now idk