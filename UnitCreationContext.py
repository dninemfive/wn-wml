from typing import Self
import DivisionCreationContext
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
import ndf_parse as ndf
from message import Message
from ndf_utils import edit_members, edit_or_read_msg
from str_utils import max_len

PADDING = max_len(rf'GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf',
                  rf'GameData\Generated\Gameplay\Gfx\ShowRoomEquivalence.ndf',
                  rf'GameData\Generated\Gameplay\Decks\DivisionPacks.ndf',
                  rf'GameData\Generated\Gameplay\Decks\DeckSerializer.ndf',
                  rf'GameData\Generated\Gameplay\Gfx\AllUnitsTactic.ndf') + len("Editing ")

class UnitCreationContext(object):
    def __init__(self: Self, context: DivisionCreationContext, unit_name: str, copy_of: str, showroom_equivalent: str | None = None):
        self.context = context
        self.internal_name = context.division.base_name(unit_name)
        self.copy_of = copy_of
        if showroom_equivalent is not None:
            self.showroom_equivalent = showroom_equivalent
        else:
            self.showroom_equivalent = copy_of

    def __enter__(self: Self):
        self.object: Object = self.copy_and_prepare_unit()
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        self.add()

    def edit(self: Self, msg: Message, path: str, padding: int = 0) -> ndf.Mod:
        return edit_or_read_msg(self.mod, msg, path, padding, True)
    
    def read(self: Self, msg: Message, path: str, padding: int = 0) -> ndf.Mod:
        return edit_or_read_msg(self.mod, msg, path, padding, False)

    @property
    def mod(self: Self) -> ndf.Mod:
        return self.context.mod

    @property
    def class_name_for_debug(self: Self):
        return f'Unit_{self.internal_name}'

    @property
    def descriptor_name(self: Self):
        return f'Descriptor_{self.class_name_for_debug}'
    
    @property
    def descriptor_path(self: Self):
        return f'$/GFX/Unit/{self.descriptor_name}'
    
    def copy_and_prepare_unit(self: Self) -> Object:
        with Message(f"Copying {self.copy_of} as {self.internal_name}") as msg:
            with self.read(msg, r'GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf', False) as unite_descriptor_ndf:
                copy: Object = unite_descriptor_ndf.by_name(f'Descriptor_Unit_{self.copy_of}').value.copy()
                edit_members(copy,
                             DescriptorId = self.context.generate_guid(self.descriptor_name),
                             ClassNameForDebug = f"'{self.class_name_for_debug}'")
                copy.namespace = self.descriptor_name
                return copy

    def add(self: Self):
        with Message(f'Adding {self.internal_name}', child_padding=PADDING) as msg:
            with self.edit(msg, rf'GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf') as unite_descriptor_ndf:
                unite_descriptor_ndf.add(ListRow(self.object, namespace=self.descriptor_name))

            with self.edit(msg, rf'GameData\Generated\Gameplay\Gfx\ShowRoomEquivalence.ndf') as showroom_equivalence_ndf:
                unit_to_showroom_equivalent: Map[MapRow] = showroom_equivalence_ndf.by_name("ShowRoomEquivalenceManager").value.by_member("UnitToShowRoomEquivalent").value
                unit_to_showroom_equivalent.add(k=self.descriptor_path, v=f"$/GFX/Unit/Descriptor_ShowRoomUnit_{self.showroom_equivalent}")
                
            with self.edit(msg, rf'GameData\Generated\Gameplay\Decks\DivisionPacks.ndf') as division_packs_ndf:
                deck_pack_descriptor = Object('DeckPackDescriptor')
                deck_pack_descriptor.add(MemberRow(self.descriptor_path, 'Unit'))
                division_packs_ndf.add(ListRow(deck_pack_descriptor, namespace=f'Descriptor_Deck_Pack_{self.internal_name}'))
                
            with self.edit(msg, rf"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf") as deck_serializer_ndf:
                deck_serializer: ListRow = deck_serializer_ndf.by_name("DeckSerializer")
                unit_ids: Map = deck_serializer.value.by_member('UnitIds').value
                unit_ids.add(k=self.descriptor_path, v=str(self.context.current_unit_id))
                
            with self.edit(msg, rf"GameData\Generated\Gameplay\Gfx\AllUnitsTactic.ndf") as all_units_tactic_ndf:
                all_units_tactic: List = all_units_tactic_ndf.by_name("AllUnitsTactic").value
                all_units_tactic.add(self.descriptor_path)

            self.context.current_unit_id += 1

    