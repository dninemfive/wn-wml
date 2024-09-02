import ndf_parse as ndf
from DivisionCreationContext import DivisionCreationContext
from metadata import DivisionMetadata, ModMetadata

mod_metadata = ModMetadata('dninemfive', '9th Infantry Division (Motorized)', r'C:/Program Files (x86)/Steam/steamapps/common/WARNO/Mods/', "0.0.0")
div_metadata = DivisionMetadata('d9', '9ID', 'US', 1390)

mod_name = '9th Infantry Division (Motorized)'
mod_path = f'{r'C:/Program Files (x86)/Steam/steamapps/common/WARNO/Mods/'}{mod_name}'
dev_name = 'd9'
mod_name_internal = f'{dev_name}_US_9ID'

mod = ndf.Mod(mod_metadata.source_path, mod_metadata.output_path)
mod.check_if_src_is_newer()

guid_cache: dict[str, str] = {}
guid_cache_path: str = "guid_cache.txt"

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

with DivisionCreationContext(mod, guid_cache_path) as context:
    context.make_division(mod_name_internal,
                          copy_of = "Descriptor_Deck_Division_US_82nd_Airborne_multi",
                          DescriptionHintTitleToken = "'ECGMWQOEZA'",
                          EmblemTexture = '"Texture_Division_Emblem_US_35th_infantry_division"')
    # make new units
    """ LOG """
    # M998 HUMVEE SUPPLY
    context.make_unit()
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

    # add a default deck to Decks.ndf (not required)