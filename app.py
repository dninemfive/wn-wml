import ndf_parse as ndf
from typing import Self, Union
from dataclasses import dataclass

mod_name = '9th Infantry Division (Motorized)'
mod_path = f'{r'C:/Program Files (x86)/Steam/steamapps/common\WARNO/Mods/'}{mod_name}'
dev_name = 'd9'
mod_name_internal = f'{dev_name}_US_9ID_(Mot)'

mod = ndf.Mod(f'{mod_path} (input)', mod_path)
mod.check_if_src_is_newer()

@dataclass
class DivisionChangeList(object):
    CfgName: str | None
    DivisionName: str | None
    DivisionPowerClassification: str | None
    DivisionNationalite: str | None
    DivisionTags: list[str] | None
    DescriptionHintTitleToken: str | None
    PackList: dict[str, int] | None
    MaxActivationPoints: int | None
    CostMatrix: dict[str, list[int]] | None
    EmblemTexture: str | None
    PortraitTexture: str | None
    TypeTexture: str | None
    CountryId: str | None

def make_division(mod: ndf.Mod, division_name: str, copy_of: str, changes: DivisionChangeList):
    # add to Divisions.ndf
    with mod.edit(r"GameData\Generated\Gameplay\Decks\Divisions.ndf") as divisions_ndf:
        original = divisions_ndf.by_name(copy_of)
    # add to DivisionList.ndf
    # add to DeckSerializer.ndf
    # add to DivisionRules.ndf
    pass

def make_unit(unit_name: str, copy_of: str, **unit_traits):
    # add unit to UniteDescriptors.ndf
    # add unit to ShowRoomEquivalence.ndf
    # add unit to DivisionPack.ndf
    pass

# make new units
""" LOG """
# M998 HUMVEE SUPPLY
# M1075 PLS
# (copy HEMTT, but with higher base XP)
# ✪ M998 HUMVEE SGT.
# ✪ M1025 HUMVEE AGL
# ✪ M1010 TC3V
""" INF """
# MOT. MP PATROL
# (just copy AB MP PATROL)
# for MOT. infantry: copy MECH. version, but reduce men to 8 and replace M240B with SAW and LAW with AT-4
# ✪ MOT. RIFLES LDR.
# MOT. RIFLES (AT-4)
# MOT. RIFLES (DRAGON)
# ✪ MOT. ENGINEERS LDR.
# MOT. ENGINEERS
# M998 HUMVEE SQC
# just copy M1038 HUMVEE
# M998 HUMVEE M2HB
# copy the AB version, but no forward deploy and normal vision
# M998 HUMVEE AGL
# copy the AB version, but no forward deploy and normal vision
""" ART """
# M198 155mm [CLU]
# M198 COPPERHEAD
# M58 MICLIC
# XM142 HIMARS [HE]
# XM142 HIMARS [CLU]
# XM142 ATACMS
# XM119 IMCS 105mm
# XM1100 120mm
""" TNK """
# XM4 AGS
# RDF/LT
# M966 HUMVEE TOW
# M1025 HUMVEE TOW
# M998 HUMVEE GLH-L
# M1025 HUMVEE AGL
""" REC """
# 👓 M998 HUMVEE M2HB
# copy 👓 M1025 HUMVEE M2HB
# 👓 FAV
# 👓 FAV AGL
# 👓 FAV TOW
# 👓 OPERATIONAL SUPPORT
# [👓] FOLT
# 👓 FWD SUPPORT [EW]
# [👓] MERCURY GREEN RPV
# [👓] MOT. SCOUTS
# copy SCOUTS, but replace M240 with SAW
# [👓] SCAT
# [[👓]] JOH-58D KIOWA
# [[👓]] M561 GAMA GOAT FAAR
""" AA """
# JOH-58C KIOWA
# M167A1 VADS 20mm
# copy AB version, remove forward deploy and add the air-transportable trait
# M998 AVENGER
# copy AB version, remove forward deploy
# M998 SETTER
# MIM-72A T-CHAPARRAL
# STINGER (TDAR)
# EXCALIBUR VWC
""" HEL """
# AH-1S COBRA
""" AIR """
# A-6E INTRUDER [HE]
# A-6E INTRUDER [CLU]
# A-6E INTRUDER [LGB]
# A-6E INTRUDER SWIP
# EA-6B PROWLER [SEAD]
# EA-6B PROWLER [EW]
# A-7E CORSAIR II [HE]
# A-7E CORSAIR II [SEAD]
# F-14B TOMCAT [AA]
# F-14B TOMCAT [LGB]
# F/A-18C [AA]
# F/A-18D [FAC]

# add new units to ShowRoomEquivalence.ndf
# add new units to AllUnitsTactic.ndf

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
    # deck_division_descriptor['PackList'] = pack_list
    # replace CostMatrix
    # set unit texture (i believe this is possible but idk how to reference the asset)
    # insert ddd into Divisions.ndf
    pass

# insert division rules in DivisionRules.ndf
# add division to DeckSerializer.ndf
# add a default deck to Decks.ndf (not required)