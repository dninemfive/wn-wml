from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Self

import warno_mfw.constants.ndf_paths as ndf_paths
import warno_mfw.context.mod_creation as ctx
import warno_mfw.utils.ndf.edit as edit
import warno_mfw.utils.ndf.ensure as ensure
import warno_mfw.utils.ndf.unit_module as modules
import warno_mfw.wrappers._modules as modules
import warno_mfw.wrappers.unit as unit_wrapper
import warno_mfw.wrappers.unit_modules.tags as tags
from warno_mfw.context.unit_module import UnitModuleContext
from warno_mfw.creators.weapon import WeaponCreator
from warno_mfw.metadata.unit import UnitMetadata
from warno_mfw.utils.ndf.decorators import ndf_path
from warno_mfw.utils.types.message import Message
from ndf_parse.model import List, ListRow, Map, MemberRow, Object
from ndf_parse.model.abc import CellValue

MODULES_DESCRIPTORS = "ModulesDescriptors"
UNIT_UI = "TUnitUIModuleDescriptor"
TAGS = "TTagsModuleDescriptor"

class UnitCreator(ABC):
    def __init__(self: Self,
                 ctx: ctx.ModCreationContext,
                 localized_name: str,
                 new_unit: str | UnitMetadata,
                 src_unit: str | UnitMetadata,
                 button_texture: str | None = None,
                 msg: Message | None = None):
        self.ctx = ctx
        self.new_unit: UnitMetadata = UnitMetadata.resolve(new_unit)
        self.src_unit: UnitMetadata = UnitMetadata.resolve(src_unit)
        self.parent_msg = msg
        self.unit = self._make_unit(localized_name, button_texture)

    def __enter__(self: Self) -> Self:
        self.msg = self.parent_msg.nest(f"Editing {self.new_unit.descriptor.name}")
        self.msg.__enter__()
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        self._apply()
        self.msg.__exit__(exc_type, exc_value, traceback)

    def _apply(self: Self):
        with self.msg.nest(f"Saving {self.new_unit.name}") as msg2:
            self.pre_apply(msg2)
            self._edit_unite_descriptor(self.ndf, msg2)
            self._edit_division_packs(self.ndf, msg2)
            self.edit_showroom_equivalence(self.ndf, msg2)
            self._edit_all_units_tactic(self.ndf, msg2)
            self.post_apply(msg2)

    # properties

    @property
    def modules(self: Self) -> modules.UnitModulesWrapper:
        return self.unit.modules

    @property
    def ndf(self: Self) -> dict[str, List]:
        return self.ctx.ndf
    
    @property
    def tags(self: Self) -> tags.TagsModuleWrapper:
        return self.modules.tags    
    
    @property
    def command_point_cost(self: Self) -> int:
        return self.modules.production.command_point_cost
    
    @command_point_cost.setter
    def command_point_cost(self: Self, value: int) -> None:
        self.modules.production.command_point_cost = value

    # abstract methods

    # virtual/abstract methods
    # virtual
    def pre_apply(self: Self, msg: Message) -> None:
        pass

    @abstractmethod
    def post_apply(self: Self, msg: Message) -> None:
        pass

    @abstractmethod
    def edit_showroom_equivalence(self: Self, ndf: List):
        pass

    # public methods

    # TODO: cache created object or smth so you don't need the weaponcreator to edit it
    def edit_weapons(self: Self, copy_of: str | None = None) -> WeaponCreator:
        if copy_of is None:
            copy_of = self.src_unit.name
        def _set_weapon_descriptor(descriptor_name: str) -> None:
            self.modules.edit_members('WeaponManager', by_name=True, Default=ensure.prefix(descriptor_name, '$/GFX/Weapon/'))
        return WeaponCreator(self.ndf, self.new_unit, copy_of, self.msg, _set_weapon_descriptor)

    # "private" methods

    def _make_unit(self: Self, localized_name: str, button_texture: str | None = None) -> unit_wrapper.UnitWrapper:
        copy: Object = self.ndf[ndf_paths.UNITE_DESCRIPTOR].by_name(self.src_unit.descriptor.name).value.copy()
        edit.members(copy,
                     DescriptorId=self.ctx.guids.generate(self.new_unit.descriptor.name),
                     ClassNameForDebug=self.new_unit.class_name_for_debug)
        with self.parent_msg.nest(f'Copying {self.src_unit.descriptor.name}') as _:
            unit = unit_wrapper.UnitWrapper(self.ctx, copy)
        unit.modules.ui.localized_name = localized_name
        if button_texture is not None:
            unit.modules.ui.ButtonTexture = button_texture
        unit.modules.tags.replace(self.src_unit.tag, self.new_unit.tag)
        unit.modules.try_edit_members('TTransportableModuleDescriptor', TransportedSoldier=f'"{self.new_unit.name}"')
        return unit
    
    # ndf edits

    @ndf_path(ndf_paths.UNITE_DESCRIPTOR)
    def _edit_unite_descriptor(self: Self, ndf: List):
        ndf.add(ListRow(self.unit.object, namespace=self.new_unit.descriptor.name, visibility="export"))

    @ndf_path(ndf_paths.DIVISION_PACKS)
    def _edit_division_packs(self: Self, ndf: List):
        deck_pack_descriptor = Object('DeckPackDescriptor')
        deck_pack_descriptor.add(MemberRow(self.new_unit.descriptor.path, "Unit"))
        ndf.add(ListRow(deck_pack_descriptor, namespace=self.new_unit.deck_pack_descriptor.name))

    @ndf_path(ndf_paths.ALL_UNITS_TACTIC)
    def _edit_all_units_tactic(self: Self, ndf: List):
        all_units_tactic = ndf.by_name("AllUnitsTactic").value
        all_units_tactic.add(self.new_unit.descriptor.path)