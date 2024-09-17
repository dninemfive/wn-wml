from dataclasses import dataclass
from typing import Self

from creators.unit import UnitCreator
from metadata.unit import UnitMetadata
from ndf_parse.model import List, MemberRow, Object
from utils.ndf import list_from_rows, to_List

UNITE_RULE = 'TDeckUniteRule'
KEY_AVAILABLE_TRANSPORT_LIST = 'AvailableTransportList'
KEY_UNIT_DESCRIPTOR = 'UnitDescriptor'
KEY_AVAILABLE_WITHOUT_TRANSPORT = 'AvailableWithoutTransport'
KEY_NUMBER_OF_UNIT_IN_PACK = 'NumberOfUnitInPack'
KEY_NUMBER_OF_UNIT_IN_PACK_XP_MULTIPLIER = 'NumberOfUnitInPackXPMultiplier'

@dataclass
class TDeckUniteRule(object):
    UnitDescriptor: str
    AvailableWithoutTransport: bool
    AvailableTransportList: list[str] | None
    NumberOfUnitInPack: int
    NumberOfUnitInPackXPMultiplier: tuple[float, float, float, float]

    @staticmethod
    def from_ndf(ndf: Object, override_transports: list[str] | None = None) -> Self:
        transports: List | None = None
        if override_transports is not None:
            transports = to_List(*override_transports)
        else:
            try:
                transports = ndf.by_member(KEY_AVAILABLE_TRANSPORT_LIST).value
            except:
                pass
        return TDeckUniteRule(
            ndf.by_member(KEY_UNIT_DESCRIPTOR).value,
            ndf.by_member(KEY_AVAILABLE_WITHOUT_TRANSPORT).value,
            transports,
            ndf.by_member(KEY_NUMBER_OF_UNIT_IN_PACK).value,
            [float(x) for x in ndf.by_member(KEY_NUMBER_OF_UNIT_IN_PACK_XP_MULTIPLIER).value]
        )

    def to_ndf(self: Self) -> Object:
        result = Object(UNITE_RULE)
        result.add(MemberRow(self.UnitDescriptor, KEY_UNIT_DESCRIPTOR))
        result.add(MemberRow(str(self.AvailableWithoutTransport), KEY_AVAILABLE_WITHOUT_TRANSPORT))
        if(self.AvailableTransportList is not None):
            result.add(MemberRow(list_from_rows(*self.AvailableTransportList), KEY_AVAILABLE_TRANSPORT_LIST))
        result.add(MemberRow(str(self.NumberOfUnitInPack), KEY_NUMBER_OF_UNIT_IN_PACK))
        result.add(MemberRow(to_List(*[str(x) for x in self.NumberOfUnitInPackXPMultiplier]), KEY_NUMBER_OF_UNIT_IN_PACK_XP_MULTIPLIER))
        return result
    
    @staticmethod
    def make(metadata: UnitMetadata | UnitCreator,
             num_per_xp: tuple[int, int, int, int],
             transports: list[str] | None = None,
             force_awt: bool | None = None) -> Self:
        if isinstance(metadata, UnitCreator):
            metadata = metadata.new
        num_per_pack = max(num_per_xp)
        xp_multipliers = [x / num_per_pack for x in num_per_xp]
        available_without_transport = force_awt if force_awt is not None else (transports is None)
        return TDeckUniteRule(
            metadata.descriptor_path,
            available_without_transport,
            transports,
            num_per_pack,
            xp_multipliers
        )