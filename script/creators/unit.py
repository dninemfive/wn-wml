from typing import Self

from constants.ndf_paths import ALL_UNITS_TACTIC, DIVISION_PACKS, SHOWROOM_EQUIVALENCE, UNITE_DESCRIPTOR
from context.module_context import ModuleContext
from metadata.new_unit import NewUnitMetadata
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow, Map, MemberRow, Object
from ndf_parse.model.abc import CellValue
from utils.ndf import edit_members, get_module, ndf_path, remove_module
from utils.types.message import Message

UNIT_UI = "TUnitUIModuleDescriptor"

class UnitCreator(object):
    def __init__(self: Self,
                 ndf: dict[str, List],
                 new_unit_metadata: NewUnitMetadata,
                 copy_of: str,
                 msg: Message | None = None):
        self.ndf = ndf
        self.localized_name = new_unit_metadata.localized_name
        self.name_token = new_unit_metadata.name_token
        self.guid = new_unit_metadata.guid
        self.new: UnitMetadata = new_unit_metadata.unit_metadata
        self.src = UnitMetadata(copy_of)
        self.root_msg = msg

    def __enter__(self: Self) -> Self:
        self.root_msg = self.root_msg.nest(f"Making {self.localized_name}")
        self.root_msg.__enter__()
        with self.root_msg.nest(f"Copying {self.src.descriptor_name}") as _:
            self.unit_object = self.make_copy(self.ndf[UNITE_DESCRIPTOR])
        self.edit_ui_module(NameToken=self.name_token)
        with self.module_context("TTagsModuleDescriptor") as tags_module:
            tag_set: List = tags_module.object.by_member("TagSet").value
            tag_set.remove(tag_set.find_by_cond(lambda x: x.value == self.src.tag))
            tag_set.add(ListRow(self.new.tag))
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        self.apply(self.ndf, self.root_msg)
        self.root_msg.__exit__(exc_type, exc_value, traceback)

    def apply(self: Self, ndf: dict[str, List], msg: Message):
        with msg.nest(f"Saving {self.new.name}") as msg2:
            self.edit_unite_descriptor(ndf, msg2)
            self.edit_division_packs(ndf, msg2)
            self.edit_showroom_equivalence(ndf, msg2)
            self.edit_all_units_tactic(ndf, msg2)

    def make_copy(self: Self, ndf: List) -> Object:
        copy: Object = ndf.by_name(self.src.descriptor_name).value.copy()
        edit_members(copy,
                     DescriptorId=self.guid,
                     ClassNameForDebug=self.new.class_name_for_debug)
        return copy

    @ndf_path(UNITE_DESCRIPTOR)
    def edit_unite_descriptor(self: Self, ndf: List):
        ndf.add(ListRow(self.unit_object, namespace=self.new.descriptor_name, visibility="export"))

    @ndf_path(SHOWROOM_EQUIVALENCE)
    def edit_showroom_equivalence(self: Self, ndf: List):
        unit_to_showroom_equivalent: Map = ndf.by_name("ShowRoomEquivalenceManager").value.by_member("UnitToShowRoomEquivalent").value
        unit_to_showroom_equivalent.add(k=self.new.descriptor_path, v=self.src.showroom_descriptor_path)

    @ndf_path(DIVISION_PACKS)
    def edit_division_packs(self: Self, ndf: List):
        deck_pack_descriptor = Object('DeckPackDescriptor')
        deck_pack_descriptor.add(MemberRow(self.new.descriptor_path, "Unit"))
        ndf.add(ListRow(deck_pack_descriptor, namespace=self.new.deck_pack_descriptor_name))

    @ndf_path(ALL_UNITS_TACTIC)
    def edit_all_units_tactic(self: Self, ndf: List):
        all_units_tactic = ndf.by_name("AllUnitsTactic").value
        all_units_tactic.add(self.new.descriptor_path)

    def module_context(self: Self, module_type: str) -> ModuleContext:
        return ModuleContext(self.unit_object, module_type)
    
    def edit_ui_module(self: Self, **changes: CellValue) -> None:
        with self.module_context(UNIT_UI) as ui_module:
            ui_module.edit_members(**changes)

    def get_module(self: Self, module_type: str) -> Object:
        result: Object | None = get_module(self.unit_object, module_type)
        return result
    
    def remove_module(self: Self, module_type: str) -> None:
        remove_module(self.unit_object, module_type)