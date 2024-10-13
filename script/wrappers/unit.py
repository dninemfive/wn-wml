from __future__ import annotations

from typing import Any, Callable, Self, Type

from metadata.unit import UnitMetadata
from wrappers._abc import NdfObjectWrapper
import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
import utils.ndf.unit_module as modules
from constants.primitive_types import MotherCountry
# from context.mod_creation import ModCreationContext
from ndf_parse.model import Object
import wrappers._modules


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
    def modules(self: Self) -> wrappers._modules.UnitModulesWrapper:
        if self._modules_descriptors is None:
            self._modules_descriptors = wrappers._modules.UnitModulesWrapper(self.ctx, self.object.by_member('ModulesDescriptors').value)
        return self._modules_descriptors
    
    def set_country(self: Self, country: str):
        country = MotherCountry.ensure_valid(country)
        self.modules.ui.CountryTexture = country
        self.modules.type.MotherCountry = country
        self.modules.type.Nationalite = ... # TODO: make a country database with members (country code, sound code, nationalite)