from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from script.context.unit_id_manager import UnitIdManager
from datetime import datetime
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
import paths
import ndf_paths
import os
import shutil
import units
import units.m1075_pls_supply
import units.m998_avenger
import units.m998_humvee_supply
import units.mot_mp_patrol

wn_metadata = WarnoMetadata(paths.WARNO_DIRECTORY)
mod_metadata = ModMetadata('dninemfive', '9th Infantry Division (Motorized)', wn_metadata, "0.0.0", 'd9', 'd99ID')
div_metadata = DivisionMetadata('d9', '9ID', 'US', 1390)

reset_source(mod_metadata, wn_metadata)

with Message(f"Creating mod {mod_metadata.name} by {mod_metadata.author}") as root_msg:
    with ModCreationContext(mod_metadata, root_msg, *ndf_paths.ALL) as mod_context:
            division_units: DivisionUnitRegistry
            with root_msg.nest("Creating units") as msg:
                division_units = DivisionUnitRegistry(DivisionRuleLookup(mod_context.ndf[ndf_paths.DIVISION_RULES],
                                                                         "US_82nd_Airborne",
                                                                         "US_8th_Inf",
                                                                         "US_11ACR",
                                                                         "US_3rd_Arm"),
                                                        msg)
                # make new units              
                # TODO: maybe default unit country?
                with UnitIdManager(mod_context, msg, div_metadata.id * 1000) as ctx:
                    # TODO: target module changes with like TModuleType:path/to/property ?
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
                    M998_HUMVEE, M1038_HUMVEE = "Descriptor_Unit_M998_Humvee_US", "Descriptor_Unit_M1038_Humvee_US"
                    BLACKHAWK, CHINOOK = "Descriptor_Unit_UH60A_Black_Hawk_US", "Descriptor_Unit_CH47_Chinook_US"
                    SMALL_UNIT_TRANSPORTS = [M998_HUMVEE, BLACKHAWK]
                    LARGE_UNIT_TRANSPORTS = [M1038_HUMVEE, BLACKHAWK]
                    division_units.register(units.mot_mp_patrol.create(ctx))
                    # units.mot_rifles_ldr.create()
                    # units.mot_rifles_at4.create()
                    # MOT. RIFLES (DRAGON)
                    division_units.register_vanilla("Rifles_half_CMD_US", 1, SMALL_UNIT_TRANSPORTS)
                    division_units.register_vanilla("Rifles_half_AT4_US", 1, SMALL_UNIT_TRANSPORTS)
                    division_units.register_vanilla("Rifles_half_Dragon_US", 1, SMALL_UNIT_TRANSPORTS)
                    division_units.register_vanilla("Rifles_Cavalry_US", 1, SMALL_UNIT_TRANSPORTS)
                    division_units.register_vanilla("Engineer_CMD_US", 1, M998_HUMVEE)
                    # MOT. ENGINEERS
                    # maybe change AB ones to fireteams?
                    division_units.register_vanilla("Airborne_CMD_US", 1, M1038_HUMVEE)
                    division_units.register_vanilla("Airborne_Dragon_US", 1, M1038_HUMVEE)
                    division_units.register_vanilla("ATteam_TOW2_US", 1, SMALL_UNIT_TRANSPORTS)
                    # transports don't get added as their own packs
                    # M998 HUMVEE M2HB
                    # copy the AB version, but no forward deploy and normal vision
                    # M998 HUMVEE AGL
                    # copy the AB version, but no forward deploy and normal vision
                    """ ART """
                    HEAVY_TRANSPORTS = [M1038_HUMVEE, CHINOOK]
                    division_units.register_vanilla("Mortier_107mm_US", 2, SMALL_UNIT_TRANSPORTS)
                    # XM1100 120mm
                    division_units.register_vanilla("Howz_M102_105mm_US", 2, SMALL_UNIT_TRANSPORTS)
                    # XM119 IMCS 105mm
                    
                    division_units.register_vanilla("Howz_M198_155mm_US", 2, HEAVY_TRANSPORTS)
                    division_units.register(units.m198_155mm_clu.create(ctx), HEAVY_TRANSPORTS)
                    division_units.register(units.m198_copperhead.create(ctx), HEAVY_TRANSPORTS)
                    # M58 MICLIC
                    # XM142 HIMARS [HE]
                    # XM142 HIMARS [CLU]
                    # XM142 ATACMS
                    """ TNK """
                    # XM4 AGS
                    # RDF/LT
                    # M966 HUMVEE TOW
                    # M1025 HUMVEE TOW
                    # M998 HUMVEE GLH-L
                    # M1025 HUMVEE AGL
                    """ REC """
                    REC_HUMVEE_M2HB, REC_HUMVEE_AGL = "Descriptor_Unit_M1025_Humvee_scout_US", "Descriptor_Unit_M1025_Humvee_AGL_nonPara_US"
                    SMALL_RECON_TRANSPORTS = [M998_HUMVEE, REC_HUMVEE_M2HB, REC_HUMVEE_AGL, BLACKHAWK]
                    division_units.register_vanilla("M981_FISTV_US", 1)
                    # 👓 M998 HUMVEE M2HB
                    # copy 👓 M1025 HUMVEE M2HB
                    # 👓 FAV
                    # 👓 FAV AGL
                    # 👓 FAV TOW
                    # 👓 OPERATIONAL SUPPORT
                    # [👓] FOLT
                    division_units.register_vanilla("Airborne_Scout_US", 1, [M998_HUMVEE, REC_HUMVEE_M2HB])
                    division_units.register_vanilla("LRRP_US", 1, SMALL_RECON_TRANSPORTS)
                    division_units.register_vanilla("Sniper_US", 1, SMALL_RECON_TRANSPORTS)
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
                    # JOH-58C KIOWA
                    # M167A1 VADS 20mm
                    # copy AB version, remove forward deploy and add the air-transportable trait
                    division_units.register(units.m998_avenger.create(ctx))
                    # M998 SETTER
                    # MIM-72A T-CHAPARRAL
                    division_units.register_vanilla("MANPAD_Stinger_C_US", 1, SMALL_UNIT_TRANSPORTS)
                    division_units.register(units.stinger_tdar.create(ctx), SMALL_UNIT_TRANSPORTS)
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
    
    generate_mod(mod_metadata, root_msg)
print(f"Generation finished at {datetime.now().time()}")