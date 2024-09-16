# right, python is stupid so i can't use type hints for this
# from context.unit_creation_context import UnitCreationContext
from context.module_context import ModuleContext
from message import Message
from metadata.unit import UnitMetadata
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue
from ndf_paths import UNITE_DESCRIPTOR
from typing import Self
from utils.ndf.misc import edit_members, ndf_path
import utils.ndf.unit_module as modules

UNIT_UI = "TUnitUIModuleDescriptor"

def ensure_quotes(s: str, quote: str = '"') -> str:
    if not s.startswith(quote):
        s = f'"{s}'
    if not s.endswith(quote):
        s = f'{s}"'
    return s


class UnitCreator(object):
    def __init__(self: Self, ctx, prefix: str, localized_name: str, country: str, copy_of: str):
        self.ctx = ctx
        self.name = localized_name
        self.new: UnitMetadata = UnitMetadata.from_localized_name(prefix, localized_name, country)
        self.src = UnitMetadata(copy_of)

    def __enter__(self: Self) -> Self:
        self.root_msg = self.ctx.root_msg.nest(f"Making {self.name}")
        self.root_msg.__enter__()
        with self.root_msg.nest(f"Copying {self.src.descriptor_name}") as _:
            self.unit_object = self.make_copy(self.ctx.ndf[UNITE_DESCRIPTOR])
        self.set_name(self.name)
        with self.module_context("TTagsModuleDescriptor") as tags_module:
            tag_set: List = tags_module.object.by_member("TagSet").value
            tag_set.remove(tag_set.find_by_cond(lambda x: x.value == f'"UNITE_{self.src.name}"'))
            tag_set.add(ListRow(self.new.tag))
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        self.apply(self.ctx.ndf, self.root_msg)
        self.root_msg.__exit__(exc_type, exc_value, traceback)

    def apply(self: Self, ndf: dict[str, List], msg: Message):
        with msg.nest(f"Saving {self.new.name}") as msg2:
            self.edit_unite_descriptor(ndf, msg2)
            self.edit_deck_serializer(ndf, msg2)
            self.edit_division_packs(ndf, msg2)
            self.edit_showroom_equivalence(ndf, msg2)
            self.edit_all_units_tactic(ndf, msg2)

    def make_copy(self: Self, ndf: List) -> Object:
        copy: Object = ndf.by_name(self.src.descriptor_name).value.copy()
        edit_members(copy,
                     DescriptorId=self.ctx.generate_guid(self.new.descriptor_name),
                     ClassNameForDebug=self.new.class_name_for_debug)
        return copy

    @ndf_path(rf'GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf')
    def edit_unite_descriptor(self: Self, ndf: List):
        ndf.add(ListRow(self.unit_object, namespace=self.new.descriptor_name, visibility="export"))

    @ndf_path(rf'GameData\Generated\Gameplay\Gfx\ShowRoomEquivalence.ndf')
    def edit_showroom_equivalence(self: Self, ndf: List):
        # TODO: allow setting this when generating the unit
        unit_to_showroom_equivalent: Map = ndf.by_name("ShowRoomEquivalenceManager").value.by_member("UnitToShowRoomEquivalent").value
        unit_to_showroom_equivalent.add(k=self.new.descriptor_path, v=self.src.showroom_descriptor_path)

    @ndf_path(rf'GameData\Generated\Gameplay\Decks\DivisionPacks.ndf')
    def edit_division_packs(self: Self, ndf: List):
        deck_pack_descriptor = Object('DeckPackDescriptor')
        deck_pack_descriptor.add(MemberRow(self.new.descriptor_path, "Unit"))
        ndf.add(ListRow(deck_pack_descriptor, namespace=self.new.deck_pack_descriptor_name))

    @ndf_path(rf"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf")
    def edit_deck_serializer(self: Self, ndf: List):
        unit_ids: Map = ndf.by_name("DeckSerializer").value.by_member('UnitIds').value
        unit_ids.add(k=self.new.descriptor_path, v=str(self.ctx.register(self.new.descriptor_name)))
        # print(str(ndf.by_name("DeckSerializer").value.by_member("UnitIds").value))
        # print(str(ndf.by_name("DeckSerializer").value.by_member("UnitIds").value.by_key(self.new.descriptor_path)))

    @ndf_path(rf"GameData\Generated\Gameplay\Gfx\AllUnitsTactic.ndf")
    def edit_all_units_tactic(self: Self, ndf: List):
        all_units_tactic = ndf.by_name("AllUnitsTactic").value
        all_units_tactic.add(self.new.descriptor_path)

    def module_context(self: Self, type_or_name: str, by_name: bool = False) -> ModuleContext:
        return ModuleContext(self.unit_object, type_or_name, by_name)
    
    def edit_ui_module(self: Self, **changes: CellValue) -> None:
        with self.module_context(UNIT_UI) as ui_module:
            ui_module.edit_members(**changes)

    def set_name(self: Self, name: str) -> None:
        self.edit_ui_module(NameToken=self.ctx.ctx.register(name))

    def add_tag(self: Self, tag: str) -> None:
        tag = ensure_quotes(tag)
        with self.module_context("TTagsModuleDescriptor") as tags_module:
            tag_set: List = tags_module.object.by_member("TagSet").value
            tag_set.add(tag)
    
    def add_tags(self: Self, *tags: str) -> None:
        for tag in tags:
            self.add_tag(tag)

    def remove_tag(self: Self, tag: str) -> None:
        tag = ensure_quotes(tag)
        with self.module_context("TTagsModuleDescriptor") as tags_module:
            tag_set: List = tags_module.object.by_member("TagSet").value
            index = tag_set.find_by_cond(lambda x: x.value == tag)
            tag_set.remove(index)

    def remove_tags(self: Self, *tags: str) -> None:
        for tag in tags:
            self.remove_tag(tag)

    # modules

    def get_module_index(self: Self, type_or_name: str, by_name: bool = False) -> int:
        return modules.get_module(self.unit_object, type_or_name, by_name)
    
    def replace_module_from(self: Self, other_unit: Object, type_or_name: str, by_name: bool = False) -> None:
        return modules.replace_module_from(self.unit_object, other_unit, type_or_name, by_name)
    
    def append_module(self: Self, module: ListRow):
        return modules.append_module(self.unit_object, module)
    
    def remove_module(self: Self, type_or_name: str, by_name: bool = False):
        return modules.remove_module(self.unit_object, type_or_name, by_name)
    
    def remove_module_by_value(self: Self, module: str):
        return modules.remove_by_value(self.unit_object, module)
    
    def append_module_from(self: Self, other_unit: Object, type_or_name: str, by_name: bool = False):
        return modules.append_module_from(self.unit_object, other_unit, type_or_name, by_name)