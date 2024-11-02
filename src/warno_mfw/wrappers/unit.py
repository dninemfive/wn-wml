from __future__ import annotations

from typing import Any, Callable, Literal, Self, Type

import warno_mfw.utils.ndf.edit as edit
import warno_mfw.utils.ndf.ensure as ensure
import warno_mfw.utils.ndf.unit_module as modules
import warno_mfw.wrappers._modules as mw
from warno_mfw.constants import enums, literals
from warno_mfw.metadata.unit import UnitMetadata
from warno_mfw.wrappers._abc import NdfObjectWrapper
# from warno_mfw.context.mod_creation import ModCreationContext
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
    
    def set_country(self: Self,
                    country: literals.MotherCountry | str,
                    nationalite: literals.Nationalite | Literal['NATO', 'PACT'] | None = None):
        self.modules.ui.CountryTexture = country
        self.modules.type.MotherCountry = country
        self.modules.type.Nationalite = nationalite if nationalite is not None else enums.nationalite(country)

    def copy(self: Self) -> Self:
        return UnitWrapper(self.ctx, self.object.copy())