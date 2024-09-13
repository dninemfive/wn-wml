from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from datetime import datetime
import units.joh_58c_kiowa
import units.m167a1_vads
import units.m198_155mm_clu
import units.m198_copperhead
import units.stinger_tdar
from utils.io import write
from message import Message, try_nest
from metadata.division_unit_registry import DivisionUnitRegistry, DivisionRuleLookup
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
import units.m1075_pls_supply
import units.m998_avenger
import units.m998_humvee_sqc
import units.m998_humvee_supply
import units.mot_mp_patrol

WARNO_DIRECTORY = rf"C:\Program Files (x86)\Steam\steamapps\common\WARNO"

wn_metadata = WarnoMetadata(WARNO_DIRECTORY)
mod_metadata = ModMetadata('dninemfive', '9th Infantry Division (Motorized)', wn_metadata, "0.0.0", 'd9', 'd99ID')
div_metadata = DivisionMetadata('d9', '9ID', 'US', 1390)    

LOCALIZATION_PATH = os.path.join(mod_metadata.folder_path, "GameData", "Localisation", mod_metadata.name, "UNITS.csv")

reset_source(mod_metadata, wn_metadata)

guid_cache_path: str = "guid_cache.txt"

with Message(f"Creating mod {mod_metadata.name} by {mod_metadata.author}") as root_msg:
    with ModCreationContext(mod_metadata, root_msg, *paths.ALL) as mod_context:
            division_units: DivisionUnitRegistry
            with root_msg.nest("Creating units") as msg:
                division_units = DivisionUnitRegistry(DivisionRuleLookup(mod_context.ndf[paths.DIVISION_RULES],
                                                                         "US_82nd_Airborne",
                                                                         "US_8th_Inf",
                                                                         "US_11ACR",
                                                                         "US_3rd_Arm"),
                                                        msg)
                # make new units
                with UnitCreationContext(mod_context, msg, div_metadata.id * 1000) as ctx:
                    """ LOG """
                    division_units.register_vanilla("FOB_US", 1)
                    division_units.register(units.m998_humvee_supply.create(ctx))
                    division_units.register(units.m1075_pls_supply.create(ctx))
                    division_units.register_vanilla("UH60A_Supply_US", 2)
                    division_units.register_vanilla("CH47_Super_Chinook_US", 1)

                    division_units.register_vanilla("OH58C_CMD_US", 1)
                    division_units.register_vanilla("UH60A_CO_US", 1)
                    division_units.register_vanilla("M577_US", 1)
                    # ✪ M998 HUMVEE SGT.
                    # ✪ M1025 HUMVEE AGL
                    # ✪ M1010 TC3V
                    """ INF """
                    M998_HUMVEE = "Descriptor_Unit_M998_Humvee_US"
                    SQUAD_CARRIER_HUMVEE = "Descriptor_Unit_d9_M998_HUMVEE_SQC_US"
                    HUMVEE_AGL = "Descriptor_Unit_d9_M998_HUMVEE_AGL_US"
                    BLACKHAWK = "Descriptor_Unit_UH60A_Black_Hawk_US"
                    SMALL_SQUAD_CARRIERS = [M998_HUMVEE, HUMVEE_AGL, BLACKHAWK]
                    LARGE_SQUAD_CARRIERS = [SQUAD_CARRIER_HUMVEE, BLACKHAWK]
                    division_units.register(units.mot_mp_patrol.create(ctx))
                    # units.mot_rifles_ldr.create()
                    # units.mot_rifles_at4.create()
                    # MOT. RIFLES (DRAGON)
                    division_units.register_vanilla("Rifles_half_CMD_US", 1, SMALL_SQUAD_CARRIERS)
                    division_units.register_vanilla("Rifles_half_AT4_US", 1, SMALL_SQUAD_CARRIERS)
                    division_units.register_vanilla("Rifles_half_Dragon_US", 1, SMALL_SQUAD_CARRIERS)
                    division_units.register_vanilla("Rifles_Cavalry_US", 1, SMALL_SQUAD_CARRIERS)
                    division_units.register_vanilla("Engineer_CMD_US", 1, [M998_HUMVEE, HUMVEE_AGL])
                    division_units.register_vanilla("Rifles_HMG_US", 1, LARGE_SQUAD_CARRIERS)
                    # MOT. ENGINEERS
                    # maybe change AB ones to fireteams?
                    division_units.register_vanilla("Airborne_CMD_US", 1)
                    division_units.register_vanilla("Airborne_Dragon_US", 1)
                    division_units.register_vanilla("ATteam_TOW2_US", 1, [M998_HUMVEE])
                    # transports don't get added as their own packs
                    units.m998_humvee_sqc.create(ctx)
                    # M998 HUMVEE M2HB
                    # copy the AB version, but no forward deploy and normal vision
                    # M998 HUMVEE AGL
                    # copy the AB version, but no forward deploy and normal vision
                    """ ART """
                    division_units.register_vanilla("Mortier_107mm_US", 2, [M998_HUMVEE])
                    # XM1100 120mm
                    division_units.register_vanilla("Howz_M102_105mm_US", 2)
                    # XM119 IMCS 105mm
                    division_units.register_vanilla("Howz_M198_155mm_US", 2)
                    division_units.register(units.m198_155mm_clu.create(ctx))
                    division_units.register(units.m198_copperhead.create(ctx))
                    # M58 MICLIC
                    # XM142 HIMARS [HE]
                    # XM142 HIMARS [CLU]
                    # XM142 ATACMS
                    """ TNK """
                    # XM4 AGS
                    # RDF/LT
                    # M966 HUMVEE TOW
                    division_units.register_vanilla("M1025_Humvee_TOW_US", 3)
                    # M998 HUMVEE GLH-L
                    # M1025 HUMVEE AGL
                    """ REC """
                    division_units.register_vanilla("M981_FISTV_US", 1)
                    # 👓 M998 HUMVEE M2HB
                    # copy 👓 M1025 HUMVEE M2HB
                    # 👓 FAV
                    # 👓 FAV AGL
                    # 👓 FAV TOW
                    # 👓 OPERATIONAL SUPPORT
                    # [👓] FOLT
                    division_units.register_vanilla("Airborne_Scout_US", 1)
                    division_units.register_vanilla("LRRP_US", 1)
                    division_units.register_vanilla("Sniper_US", 1)
                    # 👓 FWD SUPPORT [EW]
                    # [👓] MERCURY GREEN RPV
                    # [👓] MOT. SCOUTS
                    # copy SCOUTS, but replace M240 with SAW
                    # [👓] SCAT
                    division_units.register_vanilla("OH58C_Scout_US", 1)
                    division_units.register_vanilla("OH58D_Combat_Scout_US", 1)
                    division_units.register_vanilla("EH60A_EW_US", 1)
                    # [[👓]] JOH-58D KIOWA
                    # insert between OH-58D KIOWA and OH-58D KIOWA Wr.
                    # [[👓]] M561 GAMA GOAT FAAR
                    """ AA """
                    division_units.register(units.joh_58c_kiowa.create(ctx))
                    division_units.register(units.m167a1_vads.create(ctx))
                    division_units.register(units.m998_avenger.create(ctx))
                    # M998 SETTER
                    # MIM-72A T-CHAPARRAL
                    division_units.register_vanilla("MANPAD_Stinger_C_US", 1)
                    division_units.register(units.stinger_tdar.create(ctx))
                    # EXCALIBUR VWC
                    """ HEL """
                    # AH-1S COBRA
                    division_units.register_vanilla("AH1F_Cobra_US", 4)
                    division_units.register_vanilla("AH1S_Cobra_US", 4)
                    division_units.register_vanilla("AH1F_ATAS_US", 1)
                    division_units.register_vanilla("AH64_Apache_US", 2)
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
            # make division
            division_texture_name: str = mod_context.add_division_emblem(root_msg, "img/downscaled_patch.png", div_metadata) 
            mod_context.create_division(div_metadata,
                                        "Descriptor_Deck_Division_US_82nd_Airborne_multi",
                                        division_units,
                                        "Descriptor_Deck_Division_US_8th_Inf_multi",
                                        root_msg,
                                        DivisionName=mod_context.register("9TH INFANTRY DIVISION (MTZ.)"),
                                        DescriptionHintTitleToken=mod_context.register("9TH INFANTRY DIVISION (MOTORIZED)"),
                                        EmblemTexture = division_texture_name)
            # add a default deck to Decks.ndf (not required)
    with root_msg.nest("Writing localization") as msg:
        with open(LOCALIZATION_PATH, "w") as file:
             file.write(mod_context.generate_localization_csv())
    generate_mod(mod_metadata, root_msg)
print(f"Generation finished at {datetime.now().time()}")