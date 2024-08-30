import ndf_parse as ndf
from typing import Union

mod_name = '9th Infantry Division (Motorized)'
mod_path = f'{r'C:/Program Files (x86)/Steam/steamapps/common\WARNO/Mods/'}{mod_name}'
dev_name = 'd9'
mod_name_internal = f'{dev_name}_US_9ID_(Mot)'

mod = ndf.Mod(f'{mod_path} (input)', mod_path)
mod.check_if_src_is_newer()

# a list of unit descriptors to copy. Will be prepended with 'Descriptor_Unit_' and appended with '_US'
included_vanilla_units: dict[list[str]] = {
    'LOG': [
        'UH60A_Supply',
        'CH47_Super_Chinook',
        'M577',
        'UH60A_CO',
        'OH58C_CMD',
    ]
}
[
    # CH-47C SUPPLY
    # DISMOUNT. TROOPERS
    'Rifles_Cavalry',
    # FIRE TEAM (AT-4)
    'Rifles_half_AT4',
    'Rifles_half_Dragon',
    'Rifles_half_CMD',
    'Airborne_CMD',
    'Airborne_Dragon',
    'ATteam_TOW2',
    'Mortier_107mm',
    'OH58C_Scout',
    'LRRP',
    'Howz_M102_105mm',
    'Howz_M198_155mm',
    'EH60A_EW',
    'M981_FISTV',
    'Airborne_Scout',
    'OH58D_Combat_Scout'
]
# prepend with '~/Descriptor_Deck_Pack_'
included_vanilla_packs: list[str] = {
    'OH58C_CMD_US_1',
    'UH60A_Supply_US_1',
    'CH47_Super_Chinook_US_0',

}
# make new units

# make new packs

# make packlist
pack_list: dict[str, int] = {
    ('~/Descriptor_Deck_Pack_AH1F_ATAS_US', 2),
    ('~/Descriptor_Deck_Pack_AH1F_Cobra_US', 4),
    ('~/Descriptor_Deck_Pack_AH1S_Cobra_US', 4),
    ('~/Descriptor_Deck_Pack_AH64_Apache_US', 2),
    ('~/Descriptor_Deck_Pack_ATteam_TOW2_US', 2),
    ('~/Descriptor_Deck_Pack_Airborne_CMD_US', 1),
    ('~/Descriptor_Deck_Pack_Airborne_Dragon_US', 2),
    ('~/Descriptor_Deck_Pack_Airborne_Scout_US', 1),
    ('~/Descriptor_Deck_Pack_CH47_Super_Chinook_US', 2),
    ('~/Descriptor_Deck_Pack_EH60A_EW_US', 1),
    ('~/Descriptor_Deck_Pack_Engineer_CMD_US', 2),
    ('~/Descriptor_Deck_Pack_FOB_US', 1),
    ('~/Descriptor_Deck_Pack_Howz_M102_105mm_US', 2),
    ('~/Descriptor_Deck_Pack_Howz_M198_155mm_US', 2),
    ('~/Descriptor_Deck_Pack_LRRP_US', 1),
    ('~/Descriptor_Deck_Pack_M577_US', 1),
    ('~/Descriptor_Deck_Pack_M981_FISTV_US', 1),
    ('~/Descriptor_Deck_Pack_MANPAD_Stinger_C_US', 1),
    ('~/Descriptor_Deck_Pack_Mortier_107mm_US', 2),
    ('~/Descriptor_Deck_Pack_OH58C_CMD_US', 1),
    ('~/Descriptor_Deck_Pack_OH58C_Scout_US', 2),
    ('~/Descriptor_Deck_Pack_OH58D_Combat_Scout_US', 1),
    ('~/Descriptor_Deck_Pack_Ranger_Dragon_US', 1),
    ('~/Descriptor_Deck_Pack_Rifles_Cavalry_US', 1),
    ('~/Descriptor_Deck_Pack_Rifles_half_AT4_US', 1),
    ('~/Descriptor_Deck_Pack_Rifles_half_CMD_US', 1),
    ('~/Descriptor_Deck_Pack_Rifles_half_Dragon_US', 4),
    ('~/Descriptor_Deck_Pack_Sniper_US', 1),
    ('~/Descriptor_Deck_Pack_UH60A_CO_US', 1),
    ('~/Descriptor_Deck_Pack_UH60A_Supply_US', 1),
    # add new units here...
}

# make new division
with mod.edit(r'$GameData\Generated\Gameplay\Decks\Divisions.ndf') as source:
    # copy 82nd airborne
    deck_division_descriptor: dict[Union[str, list[str], dict[str, int]]] = {}
    # generate new GUID
    # assign new values
    deck_division_descriptor['CfgName'] = '{mod_name_internal}_multi'
    # assign new division name (not currently possible afaik)
    # deck_division_descriptor['DivisionName'] = hash('9th Infantry Division (Mot.)')
    # deck_division_descriptor['DescriptionHintTitleToken'] = hash(mod_name)
    # replace PackList
    # replace CostMatrix
    # set unit texture (i believe this is possible but idk how to reference the asset)
    # insert ddd into Divisions.ndf
    pass

# insert division rules in DivisionRules.ndf
# add division to DeckSerializer.ndf
# add a default deck to Decks.ndf (not required)