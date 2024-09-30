from typing import TYPE_CHECKING, Callable, Self

import constants.ndf_paths as ndf_paths
from creators.unit.abc import UnitCreator
import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
import utils.ndf.unit_module as modules
from context.unit_module import UnitModuleContext
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
    def apply(self: Self, msg: Message) -> None:
        self.edit_showroom_equivalence(self.ndf, msg)

    @ndf_path(ndf_paths.SHOWROOM_EQUIVALENCE)
    def edit_showroom_equivalence(self: Self, ndf: List):
        unit_to_showroom_equivalent: Map = ndf.by_name("ShowRoomEquivalenceManager").value.by_member("UnitToShowRoomEquivalent").value
        unit_to_showroom_equivalent.add(k=self.new_unit.descriptor_path, v=self.src_unit.showroom_descriptor_path)