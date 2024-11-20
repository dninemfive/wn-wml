from __future__ import annotations

from typing import Self

from ndf_parse.model import List, Object

import warno_mfw.creators.unit.abc as abc
import warno_mfw.utils.ndf.edit as edit
from warno_mfw import hints
from warno_mfw.hints._validation import _resolve_InfoPanelConfigurationToken, _resolve_MenuIconTexture
from warno_mfw.constants import enums
from warno_mfw.metadata.unit import UnitMetadata
from warno_mfw.utils.ndf import ensure
from warno_mfw.wrappers.str_list import StrListWrapper
from warno_mfw.wrappers.unit_modules._abc import (UnitModuleKey,
                                                  UnitModuleWrapper)


class UnitUiModuleWrapper(UnitModuleWrapper):
    _module_key = UnitModuleKey('TUnitUIModuleDescriptor')

    @property
    def ButtonTexture(self: Self) -> str:
        return self.object.by_member('ButtonTexture').value

    @ButtonTexture.setter
    def ButtonTexture(self: Self, value: str) -> None:
        edit.member(self.object, 'ButtonTexture', ensure.quoted(ensure.prefix(ensure.unquoted(value), 'Texture_Button_Unit_')))

    @property
    def CountryTexture(self: Self) -> str:
        return self.object.by_member('CountryTexture').value

    @CountryTexture.setter
    def CountryTexture(self: Self, value: hints.MotherCountry | str) -> None:
        edit.member(self.object, 'CountryTexture', ensure.quoted(ensure.prefix(ensure.unquoted(value), 'CommonTexture_MotherCountryFlag_')))

    @property
    def DisplayRoadSpeedInKmph(self: Self) -> float:
        return self.object.by_member('DisplayRoadSpeedInKmph').value

    @DisplayRoadSpeedInKmph.setter
    def DisplayRoadSpeedInKmph(self: Self, value: float) -> None:
        edit.member(self.object, 'DisplayRoadSpeedInKmph', value)

    @property
    def GenerateName(self: Self) -> bool:
        return self.object.by_member('GenerateName').value

    @GenerateName.setter
    def GenerateName(self: Self, value: bool) -> None:
        edit.member(self.object, 'GenerateName', value)

    @property
    def InfoPanelConfigurationToken(self: Self) -> str:
        return self.object.by_member('InfoPanelConfigurationToken').value

    @InfoPanelConfigurationToken.setter
    def InfoPanelConfigurationToken(self: Self, value: hints.InfoPanelConfigurationToken) -> None:
        edit.member(self.object, 'InfoPanelConfigurationToken', _resolve_InfoPanelConfigurationToken)

    @property
    def MenuIconTexture(self: Self) -> str:
        return self.object.by_member('MenuIconTexture').value

    @MenuIconTexture.setter
    def MenuIconTexture(self: Self, value: hints.MenuIconTexture | str) -> None:
        edit.member(self.object, 'MenuIconTexture', _resolve_MenuIconTexture)

    @property
    def NameToken(self: Self) -> str:
        return self.object.by_member('NameToken').value

    @NameToken.setter
    def NameToken(self: Self, value: str) -> None:
        edit.member(self.object, 'NameToken', value)

    @property
    def SpecialtiesList(self: Self) -> StrListWrapper:
        if not hasattr(self, '_specialties_list'):
            self._specialties_list = StrListWrapper(self.object.by_member('SpecialtiesList').value,
                                                    (ensure.quoted, ensure.unquoted))
        return self._specialties_list

    @SpecialtiesList.setter
    def SpecialtiesList(self: Self, value: list[hints.AnySpecialty | str] | List) -> None:
        if hasattr(self, '_specialties_list'):
            delattr(self, '_specialties_list')
        edit.member(self.object, 'SpecialtiesList', ensure.all(value, ensure.quoted))

    @property
    def TypeStrategicCount(self: Self) -> str:
        return self.object.by_member('TypeStrategicCount').value

    @TypeStrategicCount.setter
    def TypeStrategicCount(self: Self, value: hints.TypeStrategicCount | str) -> None:
        edit.member(self.object, 'TypeStrategicCount', ensure.prefix(value, 'ETypeStrategicDetailedCount/'))

    @property
    def UnitRole(self: Self) -> str:
        return self.object.by_member('UnitRole').value

    @UnitRole.setter
    def UnitRole(self: Self, value: hints.UnitRole | str) -> None:
        edit.member(self.object, 'UnitRole', enums.UnitRole.ensure_valid(value))

    @property
    def UpgradeFromUnit(self: Self) -> str | None:
        try:
            return self.object.by_member('UpgradeFromUnit').value
        except:
            return None

    @UpgradeFromUnit.setter
    def UpgradeFromUnit(self: Self, value: str | UnitMetadata | abc.UnitCreator | None) -> None:
        if isinstance(value, abc.UnitCreator):
            value = value.new_unit.descriptor.name
        elif isinstance(value, UnitMetadata):
            value = value.descriptor.name
        if value is not None:
            value = ensure.prefix(value, 'Descriptor_Unit_')
        edit.member(self.object, 'UpgradeFromUnit', value)

    def set_localized_name(self: Self, value: str) -> None:
        self.NameToken = self.ctx.localization.register(value)