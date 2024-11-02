from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Self

import warno_mfw.constants.ndf_paths as ndf_paths
from warno_mfw.creators.unit.abc import UnitCreator
from warno_mfw.metadata.unit import UnitMetadata
from warno_mfw.model.depiction_operators.weapon._abc import WeaponDepictionOperator
from ndf_parse.model import List, ListRow, Map, MemberRow, Object
from warno_mfw.utils.ndf.decorators import ndf_path
from warno_mfw.utils.types.message import Message

if TYPE_CHECKING:
    from warno_mfw.context.mod_creation import ModCreationContext

MODULES_DESCRIPTORS = "ModulesDescriptors"
UNIT_UI = "TUnitUIModuleDescriptor"
TAGS = "TTagsModuleDescriptor"

class TowedUnitCreator(UnitCreator):
    def __init__(self: Self,
                 ctx: ModCreationContext, # are you fucking kidding me
                 localized_name: str,
                 new_unit: str | UnitMetadata,
                 src_unit: str | UnitMetadata,
                 button_texture: str | None = None,
                 msg: Message | None = None,
                 *weapons: WeaponDepictionOperator):
        super().__init__(ctx, localized_name, new_unit, src_unit, button_texture, msg)
        self.weapons = weapons

    def post_apply(self: Self, msg: Message) -> None:
        self.edit_generated_depiction_vehicles(self.ndf, msg)
        self.edit_showroom_equivalence(self.ndf, msg)

    @ndf_path(ndf_paths.GENERATED_DEPICTION_VEHICLES)
    def edit_generated_depiction_vehicles(self: Self, ndf: List):
        for weapon in self.weapons:
            ndf.add(ListRow(weapon.to_ndf(), namespace=f'DepictionOperator_{self.new_unit.name}_Weapon{weapon.index}'))
        gfx_autogen: Object = ndf.by_name(self.src_unit.gfx_autogen_name).value
        # replace weapon depiction operators with new ones
        # replace Actions values with new ones
        # if specified, replace HumanSubDepictions
    