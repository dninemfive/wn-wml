import ndf_parse as ndf
from ndf_parse.model import ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue
from guid import generate_guid
from ndf_utils import edit_members

def make_division(mod: ndf.Mod,
                  division_name: str,
                  copy_of: str,
                  **changes: CellValue | None) -> None:
    print(f"adding {division_name}")
    print(f'changes: {str(changes)}')
    ddd_name = f'Descriptor_Deck_Division_{division_name}_multi'
    
    print("Divisions.ndf...", end = "")
    with mod.edit(r"GameData\Generated\Gameplay\Decks\Divisions.ndf") as divisions_ndf:
        copy: ListRow = divisions_ndf.by_name(copy_of).copy()
        edit_members(copy.value, 
                     DescriptorId = generate_guid(ddd_name),
                     CfgName = f"'{division_name}_multi'",
                     **changes)
        copy.namespace = ddd_name
        divisions_ndf.add(copy)
        # print(str(copy))
    print("Done!")

    print("DivisionList.ndf...", end = "")    
    with mod.edit(r"GameData\Generated\Gameplay\Decks\DivisionList.ndf") as division_list_ndf:
        division_list: ListRow = division_list_ndf.by_name("DivisionList")
        division_list_internal: ListRow = division_list.value.by_member("DivisionList")
        division_list_internal.value.add(f"~/{ddd_name}")
    print("Done!")
    
    print("DeckSerializer.ndf...", end = "")    
    with mod.edit(r"GameData\Generated\Gameplay\Decks\DeckSerializer.ndf") as deck_serializer_ndf:
        deck_serializer: ListRow = deck_serializer_ndf.by_name("DeckSerializer")
        division_ids: MemberRow = deck_serializer.value.by_member('DivisionIds')
        # print(str(division_ids.value))
        division_ids.value.add(k=ddd_name, v='1390')
        # print(str(division_ids))
    print("Done!")

    print("DivisionRules.ndf...", end = "")    
    with mod.edit(r"GameData\Generated\Gameplay\Decks\DivisionRules.ndf") as division_rules_ndf:
        division_rules: Map[MapRow] = division_rules_ndf.by_name("DivisionRules").value.by_member("DivisionRules").value
        copy: Object = division_rules.by_key(f"~/{copy_of}").value.copy()
        division_rules.add(k=f'~/{ddd_name}', v=copy)
        # print(str(division_rules.by_key(f'~/{ddd_name}')))
    print("Done!")

def make_unit(unit_name: str, copy_of: str, **unit_traits):
    # add unit to UniteDescriptors.ndf
    # add unit to ShowRoomEquivalence.ndf
    # add unit to DivisionPack.ndf
    # add unit to DeckSerializer.ndf
    # add unit to AllUnitsTactic.ndf
    pass