from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from datetime import datetime
import units.m1075_pls_supply
import units.m998_avenger
import units.m998_humvee_sqc
import units.m998_humvee_supply
import units.mot_mp_patrol
from utils.io import write
from message import Message, try_nest
from metadata.deck_unit_info import TDeckUniteRule
from misc.import_warno_scripts import import_script
from misc.unit_creator import UnitCreator, UNIT_UI
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from utils.bat import generate_mod, reset_source
from utils.ndf import dict_to_map, edit_members, get_module, replace_unit_module
from metadata.division import DivisionMetadata
from metadata.mod import ModMetadata
from metadata.warno import WarnoMetadata
from context.mod_creation_context import ModCreationContext
import ndf_paths as paths
import os
import shutil
import units

WARNO_DIRECTORY = rf"C:\Program Files (x86)\Steam\steamapps\common\WARNO"

wn_metadata = WarnoMetadata(WARNO_DIRECTORY)
mod_metadata = ModMetadata('dninemfive', '9th Infantry Division (Motorized)', wn_metadata, "0.0.0", 'd9', 'd99ID')
div_metadata = DivisionMetadata('d9', '9ID', 'US', 1390)    

LOCALIZATION_PATH = os.path.join(mod_metadata.folder_path, "GameData", "Localisation", mod_metadata.name, "UNITS.csv")

reset_source(mod_metadata, wn_metadata)

guid_cache_path: str = "guid_cache.txt"

# make packlist
# TODO: restructure to dict[UnitMetadata, tuple[int, TDeckUniteRule]] and have a helper method for generating these from vanilla
pack_list: dict[str, int] = {
    '~/Descriptor_Deck_Pack_AH1F_ATAS_US': 2,
    '~/Descriptor_Deck_Pack_AH1F_Cobra_US': 4,
    '~/Descriptor_Deck_Pack_AH1S_Cobra_US': 4,
    '~/Descriptor_Deck_Pack_AH64_Apache_US': 2,
    '~/Descriptor_Deck_Pack_ATteam_TOW2_US': 2,
    '~/Descriptor_Deck_Pack_Airborne_CMD_US': 1,
    '~/Descriptor_Deck_Pack_Airborne_Dragon_US': 2,
    '~/Descriptor_Deck_Pack_Airborne_Scout_US': 1,
    '~/Descriptor_Deck_Pack_CH47_Super_Chinook_US': 2,
    '~/Descriptor_Deck_Pack_EH60A_EW_US': 1,
    '~/Descriptor_Deck_Pack_Engineer_CMD_US': 2,
    '~/Descriptor_Deck_Pack_FOB_US': 1,
    '~/Descriptor_Deck_Pack_Howz_M102_105mm_US': 2,
    '~/Descriptor_Deck_Pack_Howz_M198_155mm_US': 2,
    '~/Descriptor_Deck_Pack_LRRP_US': 1,
    '~/Descriptor_Deck_Pack_M577_US': 1,
    '~/Descriptor_Deck_Pack_M981_FISTV_US': 1,
    '~/Descriptor_Deck_Pack_MANPAD_Stinger_C_US': 1,
    '~/Descriptor_Deck_Pack_Mortier_107mm_US': 2,
    '~/Descriptor_Deck_Pack_OH58C_CMD_US': 1,
    '~/Descriptor_Deck_Pack_OH58C_Scout_US': 2,
    '~/Descriptor_Deck_Pack_OH58D_Combat_Scout_US': 1,
    '~/Descriptor_Deck_Pack_Ranger_Dragon_US': 1,
    '~/Descriptor_Deck_Pack_Rifles_Cavalry_US': 1,
    '~/Descriptor_Deck_Pack_Rifles_half_AT4_US': 1,
    '~/Descriptor_Deck_Pack_Rifles_half_CMD_US': 1,
    '~/Descriptor_Deck_Pack_Rifles_half_Dragon_US': 4,
    '~/Descriptor_Deck_Pack_Sniper_US': 1,
    '~/Descriptor_Deck_Pack_UH60A_CO_US': 1,
    '~/Descriptor_Deck_Pack_UH60A_Supply_US': 1,
    # add new units here...
}
unit_data: list[tuple[tuple[str, int], TDeckUniteRule]] = []
with Message(f"Creating mod {mod_metadata.name} by {mod_metadata.author}") as root_msg:
    with ModCreationContext(mod_metadata, root_msg, *paths.ALL) as mod_context:
            with root_msg.nest("Creating units") as msg:
                # make new units              
                # TODO: maybe default unit country?
                with UnitCreationContext(mod_context, msg, div_metadata.id * 1000) as ctx:
                    # TODO: target module changes with like TModuleType:path/to/property ?
                    """ LOG """
                    unit_data.append(units.m998_humvee_supply.create(ctx))
                    unit_data.append(units.m1075_pls_supply.create(ctx))
                    # ✪ M998 HUMVEE SGT.
                    # ✪ M1025 HUMVEE AGL
                    # ✪ M1010 TC3V
                    """ INF """                    
                    unit_data.append(units.mot_mp_patrol.create(ctx))
                    # units.mot_rifles_ldr.create()
                    # units.mot_rifles_at4.create()
                    # MOT. RIFLES (DRAGON)
                    # ✪ MOT. ENGINEERS LDR.
                    # MOT. ENGINEERS
                    # transports don't get added separately
                    units.m998_humvee_sqc.create(ctx)
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
                    # insert between OH-58D KIOWA and OH-58D KIOWA Wr.
                    # [[👓]] M561 GAMA GOAT FAAR
                    """ AA """
                    # JOH-58C KIOWA
                    # M167A1 VADS 20mm
                    # copy AB version, remove forward deploy and add the air-transportable trait
                    unit_data.append(units.m998_avenger.create(ctx))
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
            for l, _ in unit_data:
                k, v = l
                pack_list[k] = v 
            # make division
            division_texture_name: str = mod_context.add_division_emblem(root_msg, "img/downscaled_patch.png", div_metadata)            

            # todo: insert this immediately after 8th Infantry Division
            mod_context.create_division(div_metadata,
                                        "Descriptor_Deck_Division_US_82nd_Airborne_multi",
                                        "Descriptor_Deck_Division_US_8th_Inf_multi",
                                        root_msg,
                                        DivisionName=mod_context.register("9TH INFANTRY DIVISION (MTZ.)"),
                                        DescriptionHintTitleToken=mod_context.register("9TH INFANTRY DIVISION (MOTORIZED)"),
                                        EmblemTexture = division_texture_name,
                                        PackList = dict_to_map(pack_list))
            # add a default deck to Decks.ndf (not required)
    with root_msg.nest("Writing localization") as msg:
        with open(LOCALIZATION_PATH, "w") as file:
             file.write(mod_context.generate_localization_csv())
    generate_mod(mod_metadata, root_msg)
print(f"Generation finished at {datetime.now().time()}")