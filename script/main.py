import os
import shutil
from datetime import datetime

import constants.ndf_paths as ndf_paths
import constants.paths as paths
import units.cmd_m998_humvee_agl
import units.cmd_m1010_tc3v
import units.cmd_mot_rifles_ldr
import units.e2c_hawkeye
import units.fav
import units.folt
import units.joh58d_kiowa
import units.m167a2_pivads_20mm
import units.m198_155mm_clu
import units.m198_copperhead
import units.m224_60mm
import units.m966_humvee_tow
import units.m998_avenger
import units.m998_humvee_agl
import units.m998_humvee_glhl
import units.m998_humvee_m2hb
import units.m998_humvee_supply
import units.m1075_pls
import units.mk19_40mm
import units.mot_engineers
import units.mot_mp_patrol
import units.mot_rifles
import units.mot_rifles_dragon
import units.mot_scouts
import units.ranger_at_section
import units.ranger_gunners
import units.rangers_m203
import units.rq_2_pioneer
import units.stinger_tdar
import units.xm85_t_chaparral
import units.xm119_imcs
import units.xm142_himars_clu
import units.xm142_himars_he
import units.xm1100_120mm
from context.mod_creation_context import ModCreationContext
from managers.unit_id import UnitIdManager
from metadata.division import DivisionMetadata
from metadata.division_unit_registry import DivisionUnitRegistry
from metadata.mod import ModMetadata
from metadata.warno import WarnoMetadata
from utils.bat import generate_mod, reset_source
from utils.types.message import Message

wn_metadata = WarnoMetadata(paths.WARNO_DIRECTORY)
mod_metadata = ModMetadata('dninemfive', '9th Infantry Division (Motorized)', wn_metadata, "0.0.0", 'd9', 'd99ID')
div_metadata = DivisionMetadata('d9', '9ID', 'US', 1390)

reset_source(mod_metadata, wn_metadata)

with Message(f"Creating mod {mod_metadata.name} by {mod_metadata.author}") as root_msg:
    with ModCreationContext(mod_metadata, root_msg, *ndf_paths.ALL) as mod_context:
            division_units: DivisionUnitRegistry
            with root_msg.nest("Creating units") as msg:
                division_units = DivisionUnitRegistry(mod_context,
                                                      div_metadata,
                                                      root_msg,
                                                      "US_82nd_Airborne",
                                                      "US_8th_Inf",
                                                      "US_11ACR",
                                                      "US_3rd_Arm",
                                                      "NATO_Garnison_Berlin")
                # make new units              
                # TODO: maybe default unit country?
                # TODO: target module changes with like TModuleType:path/to/property ?
                """ LOG """
                division_units.register_vanilla("FOB_US", 1)
                division_units.register(units.m998_humvee_supply.create(mod_context))
                division_units.register_vanilla("M35_supply_US", 1)
                division_units.register(units.m1075_pls.create(mod_context))
                division_units.register_vanilla("UH60A_Supply_US", 2)
                division_units.register_vanilla("CH47_Super_Chinook_US", 1)

                division_units.register_vanilla("OH58C_CMD_US", 1)
                division_units.register_vanilla("UH60A_CO_US", 1)
                division_units.register_vanilla("M577_US", 1)
                
                division_units.register_vanilla("M1025_Humvee_CMD_US", 1)
                division_units.register(units.cmd_m998_humvee_agl.create(mod_context))
                division_units.register(units.cmd_m1010_tc3v.create(mod_context))
                """ INF """
                M998_HUMVEE, M1038_HUMVEE = "Descriptor_Unit_M998_Humvee_US", "Descriptor_Unit_M1038_Humvee_US"
                M998_HUMVEE_M2HB, M998_HUMVEE_AGL = "Descriptor_Unit_d9_M998_HUMVEE_M2HB_US", "Descriptor_Unit_d9_M998_HUMVEE_AGL_US"
                BLACKHAWK, CHINOOK = "Descriptor_Unit_UH60A_Black_Hawk_US", "Descriptor_Unit_CH47_Chinook_US"
                SMALL_UNIT_TRANSPORTS = [M998_HUMVEE, M998_HUMVEE_M2HB, M998_HUMVEE_AGL, BLACKHAWK]
                LARGE_UNIT_TRANSPORTS = [M1038_HUMVEE, BLACKHAWK]
                # TODO: variant of the mod which doesn't reference the MP Humvee because it's a DLC unit
                division_units.register(units.mot_mp_patrol.create(mod_context), [M998_HUMVEE, "Descriptor_Unit_M1025_Humvee_MP_US"])
                division_units.register(units.cmd_mot_rifles_ldr.create(mod_context), LARGE_UNIT_TRANSPORTS)
                division_units.register(units.mot_rifles.create(mod_context), LARGE_UNIT_TRANSPORTS)
                division_units.register(units.mot_rifles_dragon.create(mod_context), LARGE_UNIT_TRANSPORTS)
                division_units.register_vanilla("Rifles_half_CMD_US", 1, SMALL_UNIT_TRANSPORTS)
                division_units.register_vanilla("Rifles_half_AT4_US", 1, SMALL_UNIT_TRANSPORTS)
                division_units.register_vanilla("Rifles_half_Dragon_US", 1, SMALL_UNIT_TRANSPORTS)
                division_units.register_vanilla("Rifles_Cavalry_US", 1, SMALL_UNIT_TRANSPORTS)
                division_units.register_vanilla("Rifles_HMG_US", 1, LARGE_UNIT_TRANSPORTS)
                division_units.register(units.rangers_m203.create(mod_context), LARGE_UNIT_TRANSPORTS)
                division_units.register(units.ranger_at_section.create(mod_context), LARGE_UNIT_TRANSPORTS)
                division_units.register(units.ranger_gunners.create(mod_context), LARGE_UNIT_TRANSPORTS)
                division_units.register_vanilla("Engineer_CMD_US", 1, [M998_HUMVEE, M998_HUMVEE_AGL])
                division_units.register(units.mot_engineers.create(mod_context), [M998_HUMVEE, M998_HUMVEE_AGL])
                division_units.register_vanilla("Airborne_CMD_US", 1, [M1038_HUMVEE])
                division_units.register_vanilla("Airborne_Dragon_US", 1, [M1038_HUMVEE])
                division_units.register_vanilla("ATteam_TOW2_US", 1, SMALL_UNIT_TRANSPORTS)
                division_units.register(units.mk19_40mm.create(mod_context), [M998_HUMVEE, M998_HUMVEE_AGL, BLACKHAWK])
                division_units.register(units.m224_60mm.create(mod_context), SMALL_UNIT_TRANSPORTS)
                """ ART """
                HEAVY_TRANSPORTS = ["Descriptor_Unit_M35_trans_US", CHINOOK]
                division_units.register_vanilla("Mortier_107mm_US", 2, SMALL_UNIT_TRANSPORTS)
                division_units.register(units.xm1100_120mm.create(mod_context))
                division_units.register_vanilla("Howz_M102_105mm_US", 2, SMALL_UNIT_TRANSPORTS)
                division_units.register(units.xm119_imcs.create(mod_context))
                division_units.register_vanilla("Howz_M198_155mm_US", 2, HEAVY_TRANSPORTS)
                division_units.register(units.m198_155mm_clu.create(mod_context), HEAVY_TRANSPORTS)
                division_units.register(units.m198_copperhead.create(mod_context), HEAVY_TRANSPORTS)
                # M58 MICLIC
                division_units.register(units.xm142_himars_he.create(mod_context))
                division_units.register(units.xm142_himars_clu.create(mod_context))
                # XM142 ATACMS
                """ TNK """
                # XM4 AGS
                # RDF/LT
                division_units.register(units.m966_humvee_tow.create(mod_context))
                division_units.register_vanilla('M1025_Humvee_TOW_US', 3)
                division_units.register(units.m998_humvee_glhl.create(mod_context))
                # transports don't get registered separately
                # M1025 HUMVEE MP
                units.m998_humvee_m2hb.create(mod_context)
                units.m998_humvee_agl.create(mod_context)
                """ REC """
                REC_HUMVEE_M2HB, REC_HUMVEE_AGL = "Descriptor_Unit_M1025_Humvee_scout_US", "Descriptor_Unit_M1025_Humvee_AGL_nonPara_US"
                SMALL_RECON_TRANSPORTS = [M998_HUMVEE, REC_HUMVEE_M2HB, REC_HUMVEE_AGL, BLACKHAWK]
                FAV = units.fav.create(mod_context).unit.descriptor_name
                division_units.register_vanilla("M981_FISTV_US", 1)
                # 👓 FAV AGL
                # 👓 FAV TOW
                # 👓 OPERATIONAL SUPPORT
                division_units.register(units.folt.create(mod_context), FAV)
                division_units.register_vanilla("LRRP_US", 2, [M998_HUMVEE, "Descriptor_Unit_M151A2_scout_US"])
                # 👓 FWD SUPPORT [EW]
                division_units.register(units.mot_scouts.create(mod_context), SMALL_RECON_TRANSPORTS)
                # [👓] SCAT
                division_units.register_vanilla("OH58C_Scout_US", 1)
                division_units.register_vanilla("OH58D_Combat_Scout_US", 1)
                division_units.register_vanilla("EH60A_EW_US", 1)
                division_units.register(units.joh58d_kiowa.create(mod_context))
                division_units.register(units.rq_2_pioneer.create(mod_context))
                division_units.register(units.e2c_hawkeye.create(mod_context))
                """ AA """
                # JOH-58C KIOWA
                division_units.register(units.m167a2_pivads_20mm.create(mod_context), [M998_HUMVEE, CHINOOK])
                division_units.register(units.m998_avenger.create(mod_context))
                # M998 SETTER
                division_units.register(units.xm85_t_chaparral.create(mod_context), [M998_HUMVEE])
                division_units.register_vanilla("MANPAD_Stinger_C_US", 1, SMALL_UNIT_TRANSPORTS)
                division_units.register(units.stinger_tdar.create(mod_context), SMALL_UNIT_TRANSPORTS)
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
            division_texture_name: str = mod_context.add_division_emblem(root_msg, "img/patch.png", div_metadata) 
            mod_context.create_division(div_metadata,
                                        "Descriptor_Deck_Division_US_82nd_Airborne_multi",
                                        division_units,
                                        "Descriptor_Deck_Division_US_8th_Inf_multi",
                                        root_msg,
                                        DivisionName=mod_context.localization.register("9TH INFANTRY DIVISION (MTZ.)"),
                                        DescriptionHintTitleToken=mod_context.localization.register("9TH INFANTRY DIVISION (MOTORIZED)"),
                                        EmblemTexture = division_texture_name)
            # add a default deck to Decks.ndf (not required)
    
    generate_mod(mod_metadata, root_msg)
print(f"Generation finished at {datetime.now().time()}")