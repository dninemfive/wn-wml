from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Self, Type

from warno_mfw.wrappers._abc import NdfObjectWrapper
from warno_mfw.wrappers.list import ListWrapper
import warno_mfw.utils.ndf.edit as edit
import warno_mfw.utils.ndf.ensure as ensure
import warno_mfw.utils.ndf.unit_module as modules
from warno_mfw.hints import MotherCountry
# from warno_mfw.context.mod_creation import ModCreationContext
from ndf_parse.model import Object
import warno_mfw.wrappers._modules

# TODO: generate literals for TAcknowUnitType and TAcknowUnitAction and TSoundFilter from AcknowDescriptors.ndf
@dataclass(frozen=True)
class Template_UnitAcknow(object):
    Identifier: str
    Filter: str # todo: TSoundFilter
class TAcknowDescriptor(NdfObjectWrapper):
    def __init__(self: Self, object: Object):
        self.object = object

    # todo


class CountryWrapper(NdfObjectWrapper):
    # ctx: ModCreationContext
    def __init__(self:          Self,
                 ctx,
                 key:           str,
                 dico_token:    str,        # UnitNamesDico.ndf
                 file_name:     str,        # UnitNames.ndf
                 # acknow_descriptors: list[TAcknowDescriptor], # might do this in the future idk
                 # sm_walk.ndf
                 # DefaultTextFormatScript can be derived from key
                 # ditto for CommonTextures.ndf (they're inconsistent in vanilla but can be consistent for the purposes of this mod)
                 # SpecificCountriesInfos can also be derived
                 ):
        self.ctx = ctx

    

    