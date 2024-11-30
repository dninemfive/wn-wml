from __future__ import annotations

from typing import Self

# from warno_mfw.context.mod_creation import ModCreationContext
from ndf_parse.model import Object

import warno_mfw.utils.ndf.edit as edit
import warno_mfw.utils.ndf.ensure as ensure
import warno_mfw.wrappers._modules as mw
from warno_mfw import hints
from warno_mfw.creators.unit.utils.traits import trait_def as td
from warno_mfw.metadata.unit import UnitMetadata
from warno_mfw.utils.ndf import misc
from warno_mfw.wrappers._abc import NdfObjectWrapper

from .unit_modules.capacite import (CapaciteModuleWrapper,
                                    create_capacite_module)


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
                    country: hints.MotherCountry | str,
                    nationalite: hints.NationaliteOrAlias | None = None):
        self.modules.ui.CountryTexture = country
        self.modules.type.MotherCountry = country
        self.modules.type.Nationalite = nationalite if nationalite is not None else misc.nationalite(country)

    def add_trait(self: Self, trait: td.TraitDef) -> None:
        if not self.modules._has_wrapper(CapaciteModuleWrapper):
            self.modules.append(create_capacite_module())
        trait.add_to(self)

    def copy(self: Self) -> Self:
        return UnitWrapper(self.ctx, self.object.copy())