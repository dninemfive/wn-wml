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

class ShowroomUnitCreator(object):
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
            self.edit_showroom_units(self.ndf, msg2)
            self.edit_showroom_equivalence(self.ndf, msg2)

    def make_copy(self: Self) -> Object:
        copy: Object = self.ndf[ndf_paths.SHOWROOM_UNITS].by_name(self.src.descriptor_name).value.copy()
        edit.members(copy,
                     DescriptorId=self.guid,
                     ClassNameForDebug=self.new.class_name_for_debug)
        return copy

    @ndf_path(ndf_paths.SHOWROOM_UNITS)
    def edit_showroom_units(self: Self, ndf: List):
        ndf.add(ListRow(self.unit_object, namespace=self.new.descriptor_name, visibility="export"))

    @ndf_path(ndf_paths.SHOWROOM_EQUIVALENCE)
    def edit_showroom_equivalence(self: Self, ndf: List):
        unit_to_showroom_equivalent: Map = ndf.by_name("ShowRoomEquivalenceManager").value.by_member("UnitToShowRoomEquivalent").value
        unit_to_showroom_equivalent.add(k=self.new.descriptor_path, v=self.showroom_src.showroom_descriptor_path)

    def edit_weapons(self: Self, copy_of: str | None = None) -> WeaponCreator:
        if copy_of is None:
            copy_of = self.src.name
        def _set_weapon_descriptor(descriptor_name: str) -> None:
            with self.module_context('WeaponManager', by_name=True) as ctx:
                ctx.edit_members(Default=ensure.prefix(descriptor_name, '$/GFX/Weapon/'))
        return WeaponCreator(self.ndf, self.new, copy_of, self.msg, _set_weapon_descriptor)

    def module_context(self: Self, type_or_name: str, by_name: bool = False) -> ModuleContext:
        return ModuleContext(self.unit_object, type_or_name, by_name)