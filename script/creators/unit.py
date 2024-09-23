from typing import Callable, Self

from creators.weapon import WeaponCreator
import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
import utils.ndf.unit_module as modules
from constants.ndf_paths import ALL_UNITS_TACTIC, DIVISION_PACKS, SHOWROOM_EQUIVALENCE, UNITE_DESCRIPTOR
from context.module_context import ModuleContext
from metadata.new_unit import NewUnitMetadata
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow, Map, MemberRow, Object
from ndf_parse.model.abc import CellValue
from utils.ndf.decorators import ndf_path
from utils.types.message import Message
import constants.ndf_paths as ndf_paths

MODULES_DESCRIPTORS = "ModulesDescriptors"
UNIT_UI = "TUnitUIModuleDescriptor"
TAGS = "TTagsModuleDescriptor"

class UnitCreator(object):
    def __init__(self: Self,
                 ndf: dict[str, List],
                 new_unit_metadata: NewUnitMetadata,
                 copy_of: str,
                 showroom_src: str | None = None,
                 button_texture_key: str | None = None,
                 msg: Message | None = None):
        self.ndf = ndf
        self.localized_name = new_unit_metadata.localized_name
        self.name_token = new_unit_metadata.name_token
        self.guid = new_unit_metadata.guid
        self.new: UnitMetadata = new_unit_metadata.unit_metadata
        self.src = UnitMetadata(copy_of)
        self.showroom_src = UnitMetadata(showroom_src) if showroom_src is not None else self.src
        self.button_texture_key = button_texture_key
        self.msg = msg

    def __enter__(self: Self) -> Self:
        self.msg = self.msg.nest(f"Making {self.localized_name}")
        self.msg.__enter__()
        with self.msg.nest(f"Copying {self.src.descriptor_name}") as _:
            self.unit_object = self.make_copy()
        self.edit_ui_module(NameToken=self.name_token)
        if self.button_texture_key is not None:
            self.edit_ui_module(ButtonTexture=self.button_texture_key)
        with self.module_context("TTagsModuleDescriptor") as tags_module:
            tag_set: List = tags_module.object.by_member("TagSet").value
            tag_set.remove(tag_set.find_by_cond(lambda x: x.value == self.src.tag))
            tag_set.add(ListRow(self.new.tag))
        try:
            with self.module_context("TTransportableModuleDescriptor") as transportable_module:
                transportable_module.edit_members(TransportedSoldier=f'"{self.new.name}"')
        except:
            pass
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        self.apply()
        self.msg.__exit__(exc_type, exc_value, traceback)

    def apply(self: Self):
        with self.msg.nest(f"Saving {self.new.name}") as msg2:
            self.edit_unite_descriptor(self.ndf, msg2)
            self.edit_division_packs(self.ndf, msg2)
            self.edit_showroom_equivalence(self.ndf, msg2)
            self.edit_all_units_tactic(self.ndf, msg2)

    def make_copy(self: Self) -> Object:
        copy: Object = self.ndf[UNITE_DESCRIPTOR].by_name(self.src.descriptor_name).value.copy()
        edit.members(copy,
                     DescriptorId=self.guid,
                     ClassNameForDebug=self.new.class_name_for_debug)
        return copy

    @ndf_path(ndf_paths.UNITE_DESCRIPTOR)
    def edit_unite_descriptor(self: Self, ndf: List):
        ndf.add(ListRow(self.unit_object, namespace=self.new.descriptor_name, visibility="export"))

    @ndf_path(ndf_paths.SHOWROOM_EQUIVALENCE)
    def edit_showroom_equivalence(self: Self, ndf: List):
        unit_to_showroom_equivalent: Map = ndf.by_name("ShowRoomEquivalenceManager").value.by_member("UnitToShowRoomEquivalent").value
        unit_to_showroom_equivalent.add(k=self.new.descriptor_path, v=self.showroom_src.showroom_descriptor_path)

    @ndf_path(ndf_paths.DIVISION_PACKS)
    def edit_division_packs(self: Self, ndf: List):
        deck_pack_descriptor = Object('DeckPackDescriptor')
        deck_pack_descriptor.add(MemberRow(self.new.descriptor_path, "Unit"))
        ndf.add(ListRow(deck_pack_descriptor, namespace=self.new.deck_pack_descriptor_name))

    @ndf_path(ndf_paths.ALL_UNITS_TACTIC)
    def edit_all_units_tactic(self: Self, ndf: List):
        all_units_tactic = ndf.by_name("AllUnitsTactic").value
        all_units_tactic.add(self.new.descriptor_path)

    def edit_weapons(self: Self, copy_of: str | None = None) -> WeaponCreator:
        if copy_of is None:
            copy_of = self.src.name
        def _set_weapon_descriptor(descriptor_name: str) -> None:
            with self.module_context('WeaponManager', by_name=True) as ctx:
                ctx.edit_members(Default=ensure.prefix(descriptor_name, '$/GFX/Weapon/'))
        return WeaponCreator(self.ndf, self.new, copy_of, self.msg, _set_weapon_descriptor)

    def module_context(self: Self, type_or_name: str, by_name: bool = False) -> ModuleContext:
        return ModuleContext(self.unit_object, type_or_name, by_name)
    
    def edit_ui_module(self: Self, **changes: CellValue) -> None:
        with self.module_context(UNIT_UI) as ui_module:
            ui_module.edit_members(**changes)

    def set_name(self: Self, name: str) -> None:
        self.edit_ui_module(NameToken=self.ctx.ctx.register(name))

    def add_tag(self: Self, tag: str) -> None:
        tag = ensure.quoted(tag)
        with self.module_context("TTagsModuleDescriptor") as tags_module:
            tag_set: List = tags_module.object.by_member("TagSet").value
            tag_set.add(tag)
    
    def add_tags(self: Self, *tags: str) -> None:
        for tag in tags:
            self.add_tag(tag)

    def remove_tag(self: Self, tag: str) -> None:
        tag = ensure.quoted(tag)
        with self.module_context("TTagsModuleDescriptor") as tags_module:
            tag_set: List = tags_module.object.by_member("TagSet").value
            index = tag_set.find_by_cond(lambda x: x.value == tag)
            tag_set.remove(index)

    def remove_tags(self: Self, *tags: str) -> None:
        for tag in tags:
            self.remove_tag(tag)

    # modules

    def get_module_index(self: Self, type_or_name: str, by_name: bool = False) -> int:
        return modules.get_index(self.unit_object, type_or_name, by_name)
    
    def get_module(self: Self, type_or_name: str, by_name: bool = False) -> Object:
        return modules.get(self.unit_object, type_or_name, by_name)
    
    def get_module_row(self: Self, type_or_name: str, by_name: bool = False) -> ListRow:
        return modules.get_row(self.unit_object, type_or_name, by_name)
    
    def replace_module(self: Self, type_or_name: str, module: CellValue, by_name: bool = False):
        return modules.replace_module(self.unit_object, module, type_or_name, by_name)
    
    def replace_module_from(self: Self, other_unit: str | Object, type_or_name: str, by_name: bool = False) -> None:
        if isinstance(other_unit, str):
            other_unit = self.get_other_unit(ensure.unit_descriptor(other_unit))
        return modules.replace_from(self.unit_object, other_unit, type_or_name, by_name)
    
    def append_module(self: Self, module: Object | ListRow):
        return modules.append(self.unit_object, module)
    
    def remove_module(self: Self, type_or_name: str, by_name: bool = False):
        return modules.remove(self.unit_object, type_or_name, by_name)
    
    def remove_module_where(self: Self, predicate: Callable[[ListRow], bool]):
        return modules.remove_where(self.unit_object, predicate)
    
    def append_module_from(self: Self, other_unit: Object, type_or_name: str, by_name: bool = False):
        return modules.append_from(self.unit_object, other_unit, type_or_name, by_name)
    
    def get_other_unit(self: Self, unit: str) -> Object:
        return self.ndf[ndf_paths.UNITE_DESCRIPTOR].by_name(ensure.unit_descriptor(unit)).value