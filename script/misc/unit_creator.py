# right, python is stupid so i can't use type hints for this
# from context.unit_creation_context import UnitCreationContext
from context.mod_creation_context import ModCreationContext
from message import Message
from metadata.unit import UnitMetadata
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_paths import UNITE_DESCRIPTOR
from typing import Self
from utils.ndf import edit_members, ndf_path, get_module, replace_unit_module

class UnitCreator(object):
    def __init__(self: Self, ctx, name: str, copy_of: str):
        self.ctx = ctx
        self.new = UnitMetadata(name)
        self.src = UnitMetadata(copy_of)

    def __enter__(self: Self) -> Self:
        self.root_msg = self.ctx.root_msg.nest(f"Making {self.new.name}")
        self.root_msg.__enter__()
        with self.root_msg.nest(f"Copying {self.src.descriptor_name}") as _:
            self.unit_object = self.make_copy(self.ctx.ndf[UNITE_DESCRIPTOR])
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
        # TODO: remove old UNITE_xxx_yy tag and replace with new one
        # tags: List = get_module(copy, 'TTagsModuleDescriptor').by_member("TagSet").value
        # tags.remove()
        return copy

    @ndf_path(rf'GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf')
    def edit_unite_descriptor(self: Self, ndf: List):
        ndf.add(ListRow(self.unit_object, namespace=self.new.descriptor_name, visibility="export"))

    @ndf_path(rf'GameData\Generated\Gameplay\Gfx\ShowRoomEquivalence.ndf')
    def edit_showroom_equivalence(self: Self, ndf: List):
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
        print(str(ndf.by_name("DeckSerializer").value.by_member("UnitIds").value.by_key(self.new.descriptor_path)))

    @ndf_path(rf"GameData\Generated\Gameplay\Gfx\AllUnitsTactic.ndf")
    def edit_all_units_tactic(self: Self, ndf: List):
        all_units_tactic = ndf.by_name("AllUnitsTactic").value
        all_units_tactic.add(self.new.descriptor_path)

    def get_module(self: Self, module_type: str) -> Object:
        # print(f"Trying to get module {module_type} on {self.new.class_name_for_debug}")
        result: Object | None = get_module(self.unit_object, module_type)
        # print(str(result))
        return result