import ndf_parse as ndf
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue
from ndf_utils import edit_members
from io_utils import load, write
from uuid import uuid4
from typing import Self
from metadata import DivisionMetadata
from message import Message

class DivisionCreationContext(object):
    def __init__(self: Self, mod: ndf.Mod, division: DivisionMetadata, guid_cache_path: str):
        self.mod = mod
        self.division = division
        self.guid_cache_path = guid_cache_path
        self.guid_cache: dict[str, str] = load(guid_cache_path, {})
        # todo: cache to ensure this stays constant even if user reorders unit declarations
        self.current_unit_id: int = division.id * 1000

    # https://peps.python.org/pep-0343/
    # https://docs.python.org/3/reference/datamodel.html#context-managers
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        write(self.guid_cache, self.guid_cache_path)

    @property
    def division_name_internal(self):
        return f'{self.division.dev_short_name}_{self.division.short_name}_{self.division.country}'

    def generate_guid(self: Self, guid_key: str | None) -> str:
        """ Generates a GUID in the format NDF expects """
        if guid_key in self.guid_cache:
            return self.guid_cache[guid_key]
        result: str = f'GUID:{{{str(uuid4())}}}'
        self.guid_cache[guid_key] = result
        return result
    
    def edit(self: Self, msg: Message, path: str) -> ndf.Mod:
        with msg.nest(f'\tEditing {path}') as _:
            return self.mod.edit(path)

    def make_division(self: Self,
                      copy_of: str,
                    **changes: CellValue | None) -> None:
        with Message(f"Making division {self.division.short_name}") as msg:
            ddd_name = f'Descriptor_Deck_Division_{self.division_name_internal}_multi'
            
            with self.edit(msg, r"GameData\Generated\Gameplay\Decks\Divisions.ndf") as divisions_ndf:
                copy: ListRow = divisions_ndf.by_name(copy_of).copy()
                edit_members(copy.value, 
                            DescriptorId = self.generate_guid(ddd_name),
                            CfgName = f"'{self.division_name_internal}_multi'",
                            **changes)
                copy.namespace = ddd_name
                divisions_ndf.add(copy)
                
            with self.edit(msg, r"GameData\Generated\Gameplay\Decks\DivisionList.ndf") as division_list_ndf:
                division_list: List = division_list_ndf.by_name("DivisionList").value.by_member("DivisionList").value
                division_list.add(f"~/{ddd_name}")
            
            with self.edit(msg, r"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf") as deck_serializer_ndf:
                division_ids: Map = deck_serializer_ndf.by_name("DeckSerializer").value.by_member('DivisionIds').value
                division_ids.add(k=ddd_name, v=str(self.division.id))
                
            with self.edit(msg, r"GameData\Generated\Gameplay\Decks\DivisionRules.ndf") as division_rules_ndf:
                division_rules: Map[MapRow] = division_rules_ndf.by_name("DivisionRules").value.by_member("DivisionRules").value
                copy: Object = division_rules.by_key(f"~/{copy_of}").value.copy()
                division_rules.add(k=f'~/{ddd_name}', v=copy)

    def copy_and_prepare_unit(self: Self, unit_name: str, copy_of: str) -> Object:
        class_name_for_debug = f'Unit_{self.division.dev_short_name}_{unit_name}_{self.division.country}'
        descriptor_name = f'Descriptor_{class_name_for_debug}'
        with Message(f"Copying {copy_of} as {unit_name}") as msg:
            with self.mod.edit(r'GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf', False) as unite_descriptor_ndf:
                copy: ListRow = unite_descriptor_ndf.by_name(f'Descriptor_Unit_{copy_of}').copy()
                edit_members(copy.value, DescriptorId = self.generate_guid(descriptor_name), ClassNameForDebug = f"'{class_name_for_debug}'")
                copy.namespace = descriptor_name

    def add_unit(self: Self, unit_name: str, unit: Object, showroom_equivalent: str):
        base_unit_name = f'{self.division.dev_short_name}_{unit_name}_{self.division.country}'
        unit_descriptor_namespace = f'Descriptor_Unit_{base_unit_name}'
        with Message(f'Adding {unit}') as msg:
            with self.edit(r'GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf') as unite_descriptor_ndf:
                unite_descriptor_ndf.add(ListRow(unit, namespace=unit_descriptor_namespace))
            unit_descriptor_path = f'$/GFX/Unit/{unit_descriptor_namespace}'
            # add unit to ShowRoomEquivalence.ndf
            with self.edit(r'GameData\Generated\Gameplay\Gfx\ShowRoomEquivalence.ndf') as showroom_equivalence_ndf:
                unit_to_showroom_equivalent: Map[MapRow] = showroom_equivalence_ndf.by_name("ShowRoomEquivalenceManager").value.by_member("UnitToShowRoomEquivalent").value
                unit_to_showroom_equivalent.add(k=unit_descriptor_path, v=f"$/GFX/Unit/Descriptor_ShowRoomUnit_{showroom_equivalent}")
            # add unit to DivisionPacks.ndf
            with self.edit(r'r"GameData\Generated\Gameplay\Decks\DivisionPacks.ndf') as division_packs_ndf:
                deck_pack_descriptor = Object('DeckPackDescriptor')
                deck_pack_descriptor.add(MemberRow(unit_descriptor_path, 'Unit'))
                division_packs_ndf.add(ListRow(deck_pack_descriptor, namespace=f'Descriptor_Deck_Pack_{base_unit_name}'))
            # add unit to DeckSerializer.ndf
            with self.edit(r"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf") as deck_serializer_ndf:
                deck_serializer: ListRow = deck_serializer_ndf.by_name("DeckSerializer")
                unit_ids: Map = deck_serializer.value.by_member('UnitIds').value
                unit_ids.add(k=unit_descriptor_path, v=str(self.current_unit_id))
            # add unit to AllUnitsTactic.ndf
            with self.edit(r"GameData\Generated\Gameplay\Gfx\AllUnitsTactic.ndf") as all_units_tactic_ndf:
                all_units_tactic: List = all_units_tactic_ndf.by_name("AllUnitsTactic").value
                all_units_tactic.add(unit_descriptor_path)

            self.current_unit_id += 1
        

    def make_unit(self: Self, unit_name: str, copy_of: str, showroom_unit: str, **unit_traits):
        class_name_for_debug = f'Unit_{self.division.dev_short_name}_{unit_name}_{self.division.country}'
        descriptor_name = f'Descriptor_{class_name_for_debug}'
        descriptor_path = f'$/GFX/Unit/{descriptor_name}'
        # add unit to UniteDescriptors.ndf
        with self.mod.edit(r'GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf') as unite_descriptor_ndf:
            copy: ListRow = unite_descriptor_ndf.by_name(copy_of).copy()
            edit_members(copy.value, 
                        DescriptorId = self.generate_guid(descriptor_name),
                        ClassNameForDebug = f"'{class_name_for_debug}'",
                        **unit_traits)
            copy.namespace = descriptor_name
            unite_descriptor_ndf.add(copy)