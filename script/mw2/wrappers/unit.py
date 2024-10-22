from __future__ import annotations

from typing import Any, Callable, Self, Type

import mw2.utils.ndf.edit as edit
import mw2.utils.ndf.ensure as ensure
import mw2.utils.ndf.unit_module as modules
import mw2.wrappers._modules as mw
from mw2.constants.primitive_types import MotherCountry
from mw2.metadata.unit import UnitMetadata
from mw2.wrappers._abc import NdfObjectWrapper
# from context.mod_creation import ModCreationContext
from ndf_parse.model import Object


class UnitWrapper(NdfObjectWrapper):
    # ctx: ModCreationContext
    def __init__(self: Self, ctx, object: Object):
        self.ctx = ctx
        self.object = object
        self._modules_descriptors = None

    @property
    def DescriptorId(self: Self) -> str:
        return ensure.no_prefix_or_suffix(self._get('DescriptorId'), 'GUID:{', '}')
    
    @DescriptorId.setter
    def DescriptorId(self: Self, value: str) -> None:
        return self._set('DescriptorId', ensure.guid(value))
        
    @property
    def ClassNameForDebug(self: Self) -> str:
        return ensure.unquoted(self.object.by_member('ClassNameForDebug').value)
    
    @ClassNameForDebug.setter
    def ClassNameForDebug(self: Self, value: str | UnitMetadata) -> None:
        if isinstance(value, UnitMetadata):
            value = value.class_name_for_debug
        edit.members(self.object,
                     ClassNameForDebug=ensure.quoted(value))

    @property
    def modules(self: Self) -> mw.UnitModulesWrapper:
        if self._modules_descriptors is None:
            self._modules_descriptors = mw.UnitModulesWrapper(self.ctx, self.object.by_member('ModulesDescriptors').value)
        return self._modules_descriptors
    
    def set_country(self: Self, country: str):
        raise NotImplemented
        country = MotherCountry.ensure_valid(country)
        self.modules.ui.CountryTexture = country
        self.modules.type.MotherCountry = country
        self.modules.type.Nationalite = ... # TODO: make a country database with members (country code, sound code, nationalite)

    def copy(self: Self) -> Self:
        return UnitWrapper(self.ctx, self.object.copy())