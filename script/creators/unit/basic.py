from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Self

import constants.ndf_paths as ndf_paths
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

class BasicUnitCreator(UnitCreator):
    def __init__(self: Self,
                 ctx: ModCreationContext, # are you fucking kidding me
                 localized_name: str,
                 new_unit: str | UnitMetadata,
                 src_unit: str | UnitMetadata,
                 gfx_unit: str | UnitMetadata | None = None,
                 button_texture: str | None = None,
                 msg: Message | None = None):
        super().__init__(ctx, localized_name, new_unit, src_unit, button_texture, msg)
        self.gfx_unit = UnitMetadata.resolve(gfx_unit) if gfx_unit is not None else self.src_unit

    def pre_apply(self: Self, msg: Message) -> None:
        self.unit.modules.replace_from(self.ctx.get_unit(self.gfx_unit.descriptor_name), 'ApparenceModel', by_name=True)

    def post_apply(self: Self, msg: Message) -> None:
        self.edit_showroom_units(self.ndf, msg)
        self.edit_showroom_equivalence(self.ndf, msg)

    @ndf_path(ndf_paths.SHOWROOM_UNITS)
    def edit_showroom_units(self: Self, ndf: List):
        copy: UnitWrapper = self.ctx.get_unit(self.gfx_unit.name, showroom=True)
        copy.DescriptorId = self.ctx.guids.generate(self.new_unit.showroom_descriptor_name)
        copy.modules.type.copy(self.unit.modules.type.object)
        # TODO: check if the unit actually has a weapon descriptor to reference
        # try:
        #     copy.modules.remove_where(lambda x: isinstance(x.value, str) and x.value.startswith('$/GFX/Weapon/WeaponDescriptor_'))
        #     copy.modules.append(self.new_unit.weapon_descriptor_path)
        # except:
        #     pass
        # for vehicles with replaced turret models, will have to make a new TacticVehicleDepictionTemplate and add it to GeneratedDepictionVehicles.ndf
        # and then set the depiction path here
        ndf.add(ListRow(copy.object, visibility='export', namespace=self.new_unit.showroom_descriptor_name))

    @ndf_path(ndf_paths.SHOWROOM_EQUIVALENCE)
    def edit_showroom_equivalence(self: Self, ndf: List):
        unit_to_showroom_equivalent: Map = ndf.by_name("ShowRoomEquivalenceManager").value.by_member("UnitToShowRoomEquivalent").value
        unit_to_showroom_equivalent.add(k=self.new_unit.descriptor_path, v=self.new_unit.showroom_descriptor_path)