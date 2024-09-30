from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Self

import constants.ndf_paths as ndf_paths
from script.wrappers.unit_modules.unit_ui import UnitUiModuleWrapper
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
from wrappers.unit import UnitWrapper

if TYPE_CHECKING:
    from context.mod_creation import ModCreationContext

MODULES_DESCRIPTORS = "ModulesDescriptors"
UNIT_UI = "TUnitUIModuleDescriptor"
TAGS = "TTagsModuleDescriptor"

class UnitCreatorABC(ABC):
    def __init__(self: Self,
                 ctx,#: ModCreationContext, # are you fucking kidding me
                 localized_name: str,
                 new_unit: str | UnitMetadata,
                 src_unit: str | UnitMetadata,
                 button_texture_key: str | None = None,
                 msg: Message | None = None):
        self.ctx = ctx
        self.localized_name = localized_name
        self.new_unit: UnitMetadata = UnitMetadata.resolve(new_unit)
        self.src_unit: UnitMetadata = UnitMetadata.resolve(src_unit)
        self.button_texture_key = button_texture_key
        self.parent_msg = msg

    def __enter__(self: Self) -> Self:
        self.msg = self.parent_msg.nest(f"Making {self.localized_name}")
        self.msg.__enter__()
        with self.msg.nest(f"Copying {self.src_unit.descriptor_name}") as _:
            self.unit = UnitWrapper(self._make_unit())
        self.unit.modules.ui.localized_name = self.localized_name
        if self.button_texture_key is not None:
            self.edit_ui_module(ButtonTexture=self.button_texture_key)
        with self.module_context("TTagsModuleDescriptor") as tags_module:
            tag_set: List = tags_module.object.by_member("TagSet").value
            tag_set.remove(tag_set.find_by_cond(lambda x: x.value == self.src_unit.tag))
            tag_set.add(ListRow(self.new_unit.tag))
        try:
            with self.module_context("TTransportableModuleDescriptor") as transportable_module:
                transportable_module.edit_members(TransportedSoldier=f'"{self.new_unit.name}"')
        except:
            pass
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        self._apply_all()
        self.msg.__exit__(exc_type, exc_value, traceback)

    def _apply_all(self: Self):
        with self.msg.nest(f"Saving {self.new_unit.name}") as msg2:
            self._edit_unite_descriptor(self.ndf, msg2)
            self._edit_division_packs(self.ndf, msg2)
            self.edit_showroom_equivalence(self.ndf, msg2)
            self._edit_all_units_tactic(self.ndf, msg2)
            self.apply(msg2)

    # properties

    @property
    def ndf(self: Self) -> dict[str, List]:
        return self.ctx.ndf

    # abstract methods

    @abstractmethod
    def apply(self: Self, msg: Message) -> None:
        pass
    
    @ndf_path(ndf_paths.SHOWROOM_EQUIVALENCE)
    @abstractmethod
    def edit_showroom_equivalence(self: Self, ndf: List):
        pass

    # public methods

    # TODO: cache created object or smth so you don't need the weaponcreator to edit it
    def edit_weapons(self: Self, copy_of: str | None = None) -> WeaponCreator:
        if copy_of is None:
            copy_of = self.src_unit.name
        def _set_weapon_descriptor(descriptor_name: str) -> None:
            with self.module_context('WeaponManager', by_name=True) as ctx:
                ctx.edit_members(Default=ensure.prefix(descriptor_name, '$/GFX/Weapon/'))
        return WeaponCreator(self.ndf, self.new_unit, copy_of, self.msg, _set_weapon_descriptor)

    # "private" methods

    def _make_unit(self: Self, localized_name: str, button_texture: str | None = None) -> Object:
        copy: Object = self.ndf[ndf_paths.UNITE_DESCRIPTOR].by_name(self.src_unit.descriptor_name).value.copy()
        edit.members(copy,
                     DescriptorId=self.ctx.guids.generate(self.new_unit.descriptor_name),
                     ClassNameForDebug=self.new_unit.class_name_for_debug)
        with self.msg.nest(f'Copying {self.src_unit.descriptor_name}') as msg:
            self.unit = UnitWrapper(self.ctx, copy)
        self.unit.modules.ui.localized_name = localized_name
        if self.button_texture_key is not None:
            self.unit.modules.ui.ButtonTexture = button_texture
        self.unit.modules.tags.replace(self.src_unit.tag, self.new_unit.tag)
        return copy
        try:
            with self.module_context("TTransportableModuleDescriptor") as transportable_module:
                transportable_module.edit_members(TransportedSoldier=f'"{self.new_unit.name}"')
        except:
            pass
        return self
    
    # ndf edits

    @ndf_path(ndf_paths.UNITE_DESCRIPTOR)
    def _edit_unite_descriptor(self: Self, ndf: List):
        ndf.add(ListRow(self.unit, namespace=self.new_unit.descriptor_name, visibility="export"))

    @ndf_path(ndf_paths.DIVISION_PACKS)
    def _edit_division_packs(self: Self, ndf: List):
        deck_pack_descriptor = Object('DeckPackDescriptor')
        deck_pack_descriptor.add(MemberRow(self.new_unit.descriptor_path, "Unit"))
        ndf.add(ListRow(deck_pack_descriptor, namespace=self.new_unit.deck_pack_descriptor_name))

    @ndf_path(ndf_paths.ALL_UNITS_TACTIC)
    def _edit_all_units_tactic(self: Self, ndf: List):
        all_units_tactic = ndf.by_name("AllUnitsTactic").value
        all_units_tactic.add(self.new_unit.descriptor_path)


    