from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Self

import constants.ndf_paths as ndf_paths
from script.utils import localization
from wrappers.unit import UnitWrapper
import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
import utils.ndf.unit_module as modules
from context.unit_module import UnitModuleContext
from creators.unit.abc import UnitCreator
from creators.weapon import WeaponCreator
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow, Map, MemberRow, Object
from ndf_parse.model.abc import CellValue
from utils.ndf.decorators import ndf_path
from utils.types.message import Message

if TYPE_CHECKING:
    from context.mod_creation import ModCreationContext

MODULES_DESCRIPTORS = "ModulesDescriptors"
UNIT_UI = "TUnitUIModuleDescriptor"
TAGS = "TTagsModuleDescriptor"

class TowedUnitCreator(UnitCreator):
    def __init__(self: Self,
                 ctx: ModCreationContext, # are you fucking kidding me
                 localized_name: str,
                 new_unit: str | UnitMetadata,
                 src_unit: str | UnitMetadata,
                 weapon: str,
                 button_texture: str | None = None,
                 msg: Message | None = None):
        super().__init__(ctx, localized_name, new_unit, src_unit, weapon, button_texture, msg)
        self.weapon = weapon

    def apply(self: Self, msg: Message) -> None:
        self.edit_showroom_units(self.ndf, msg)
        self.edit_showroom_equivalence(self.ndf, msg)

    