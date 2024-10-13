from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Self

import constants.ndf_paths as ndf_paths
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

class BasicUnitCreator(UnitCreator):
    def __init__(self: Self,
                 ctx,#: ModCreationContext, # are you fucking kidding me
                 localized_name: str,
                 new_unit: str | UnitMetadata,
                 src_unit: str | UnitMetadata,
                 showroom_unit: str | UnitMetadata | None = None,
                 button_texture: str | None = None,
                 msg: Message | None = None):
        self.ctx = ctx
        self.new_unit: UnitMetadata = UnitMetadata.resolve(new_unit)
        self.src_unit: UnitMetadata = UnitMetadata.resolve(src_unit)
        self.showroom_unit = UnitMetadata.resolve(showroom_unit) if showroom_unit is not None else self.src_unit
        self.parent_msg = msg
        self.unit = self._make_unit(localized_name, button_texture)

    def apply(self: Self, msg: Message) -> None:
        self.edit_showroom_equivalence(self.ndf, msg)

    @ndf_path(ndf_paths.SHOWROOM_UNITS)
    def edit_showroom_equivalence(self: Self, ndf: List):
        copy: Object = ndf.by_name(self.showroom_unit.showroom_descriptor_name).value.copy()
        copy.by_member('DescriptorId').value = self.ctx.guids.generate(self.new_unit.showroom_descriptor_name)
        # replace type module descriptor
        # replace weapon descriptor
        ndf.add(ListRow(copy, visibility='export', namespace=self.new_unit.showroom_descriptor_name))

    @ndf_path(ndf_paths.SHOWROOM_EQUIVALENCE)
    def edit_showroom_equivalence(self: Self, ndf: List):
        unit_to_showroom_equivalent: Map = ndf.by_name("ShowRoomEquivalenceManager").value.by_member("UnitToShowRoomEquivalent").value
        unit_to_showroom_equivalent.add(k=self.new_unit.descriptor_path, v=self.new_unit.showroom_descriptor_path)