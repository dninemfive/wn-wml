from dataclasses import dataclass
from typing import Self

from managers.guid import GuidManager
from managers.localization import LocalizationManager
from metadata.unit import UnitMetadata


@dataclass
class NewUnitMetadata(object):
    localized_name: str
    name_token: str
    guid: str
    unit_metadata: str

    @staticmethod
    def from_(prefix: str, localized_name: str, country: str, guids: GuidManager, localization: LocalizationManager) -> Self:
        metadata = UnitMetadata.from_localized_name(prefix, localized_name, country)
        return NewUnitMetadata(localized_name, localization.register(localized_name), guids.generate(metadata.descriptor_name), metadata)