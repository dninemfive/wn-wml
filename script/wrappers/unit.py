from curses import wrapper
from typing import Any, Callable, Self, Type

from wrappers.unit_modules._modules import UnitModulesWrapper
from wrappers.unit_modules.unit_ui import UnitUiModuleWrapper
import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
import utils.ndf.unit_module as modules
# from context.mod_creation import ModCreationContext
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue
from wrappers.unit_modules.tags import TagsModuleWrapper
from wrappers.unit_modules.type_unit import TypeUnitModuleWrapper
from constants.primitive_types import MotherCountry

from wrappers.unit_modules._abc import UnitModuleWrapper, UnitModuleKey


class UnitWrapper(object):
    # ctx: ModCreationContext
    def __init__(self: Self, ctx, object: Object):
        self.ctx = ctx
        self.object = object

    @property
    def modules(self: Self) -> UnitModulesWrapper:
        if self._modules_descriptors is None:
            self._modules_descriptors = UnitModulesWrapper(self.object.by_member('ModulesDescriptors').value)
        return self._modules_descriptors
    
    def set_country(self: Self, country: str):
        country = MotherCountry.ensure_valid(country)
        self.modules.ui.CountryTexture = country
        self.modules.type.MotherCountry = country
        self.modules.type.Nationalite = ... # TODO: make a country database with members (country code, sound code, nationalite)