from context.unit_creation_context import UnitCreationContext
from context.ndf_context import NdfContext
from message import Message
from metadata.unit import UnitMetadata
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from typing import Self
from utils.ndf import edit_members, ndf_path

class UnitCreator(object):
    def __init__(self: Self, ctx: UnitCreationContext, name: str, copy_of: str):
        self.ctx = ctx
        self.meta = UnitMetadata(f'{ctx.prefix}_{name}')
        self.copy_of = UnitMetadata(copy_of)

    def apply(self: Self, ndf: dict[str, List], msg: Message):
        with msg.nest(f"Adding {self.meta.name}") as _:
            self.edit_unite_descriptor(ndf, msg)

    @ndf_path(rf'GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf')
    def edit_unite_descriptor(self: Self, ndf: List):
        copy = ndf.by_name(self.copy_of.descriptor_name).value.copy()
        edit_members(copy,
                     DescriptorId=self.ctx.generate_guid(self.meta.descriptor_name),
                     ClassNameForDebug=self.meta.class_name_for_debug)
        ndf.add(ListRow(copy, namespace=self.meta.descriptor_name, visibility="export"))

    @ndf_path(rf'GameData\Generated\Gameplay\Gfx\ShowRoomEquivalence.ndf')
    def edit_showroom_equivalence(self: Self, ndf: List):
        unit_to_showroom_equivalent: Map = ndf.by_name("ShowRoomEquivalenceManager").value.by_member("UnitToShowRoomEquivalent").value
        unit_to_showroom_equivalent.add(k=self.meta.descriptor_path, v=self.copy_of.showroom_descriptor_path)

    @ndf_path(rf'GameData\Generated\Gameplay\Decks\DivisionPacks.ndf')
    def edit_division_packs(self: Self, ndf: List):
        deck_pack_descriptor = Object('DeckPackDescriptor')
        deck_pack_descriptor.add(MemberRow(self.meta.descriptor_path, "Unit"))
        ndf.add(ListRow(deck_pack_descriptor, namespace=f"Descriptor_Deck_Pack_{self.meta.name}"))

    @ndf_path(rf"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf")
    def edit_deck_serializer(self: Self, ndf: List):
        deck_serializer: ListRow = ndf.by_name("DeckSerializer")
        unit_ids: Map = deck_serializer.value.by_member('UnitIds').value
        unit_ids.add(k=self.meta.descriptor_path, v=str(self.ctx.register(self.meta.descriptor_name)))

    @ndf_path(rf"GameData\Generated\Gameplay\Gfx\AllUnitsTactic.ndf")
    def edit_all_units_tactic(self: Self, ndf: List):
        all_units_tactic = ndf.by_name("AllUnitsTactic").value
        all_units_tactic.add(self.meta.descriptor_path)