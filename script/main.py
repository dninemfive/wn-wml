from __future__ import annotations

from datetime import datetime
from typing import Callable

import mw2.constants.ndf_paths as ndf_paths
import mw2.constants.paths as paths
from div_9id import ammo
from div_9id.units import AA, ART, HEL, INF, LOG, REC, TNK
from mw2.context.mod_creation import ModCreationContext
from mw2.metadata.division import DivisionMetadata
from mw2.metadata.mod import ModMetadata
from mw2.metadata.warno import WarnoMetadata
from mw2.unit_registration.division_unit_registry import DivisionUnitRegistry
from mw2.unit_registration.unit_group import UnitGroup
from mw2.utils.bat import reset_source
from mw2.utils.types.message import Message

wn_metadata = WarnoMetadata(paths.WARNO_DIRECTORY)
mod_metadata = ModMetadata('dninemfive', '9th Infantry Division (Motorized)', wn_metadata, "0.0.0", 'd9', 'd99ID')
div_metadata = DivisionMetadata('d9', '9ID', 'US', 1390)

reset_source(mod_metadata, wn_metadata)

with Message(f"Creating mod {mod_metadata.name} by {mod_metadata.author}") as root_msg:
    with ModCreationContext(mod_metadata, root_msg, *ndf_paths.ALL) as mod_context:
            ammo.fgr_17_viper.create(mod_context)
            ammo.m60e3.create(mod_context)
            ammo.m203.create(mod_context)
            division_units: DivisionUnitRegistry
            with root_msg.nest("Creating units") as msg:
                division_units = DivisionUnitRegistry(mod_context,
                                                      div_metadata,
                                                      root_msg,
                                                      "US_82nd_Airborne",
                                                      "US_8th_Inf",
                                                      "US_11ACR",
                                                      "US_3rd_Arm",
                                                      "NATO_Garnison_Berlin",
                                                      "US_101st_Airmobile")
                # make new units              
                # TODO: maybe default unit country?
                # TODO: target module changes with like TModuleType:path/to/property ?       
                for category in [LOG, INF, ART, TNK, REC, AA, HEL]:
                    group: Callable[[DivisionUnitRegistry, Message], UnitGroup] = getattr(category, 'group')
                    group(division_units, msg).register_all()         
                
                """ INF """
                M998_HUMVEE, M1038_HUMVEE = "Descriptor_Unit_M998_Humvee_US", "Descriptor_Unit_M1038_Humvee_US"
                M998_HUMVEE_M2HB, M998_HUMVEE_AGL = "Descriptor_Unit_d9_M998_HUMVEE_M2HB_US", "Descriptor_Unit_d9_M998_HUMVEE_AGL_US"
                BLACKHAWK, CHINOOK = "Descriptor_Unit_UH60A_Black_Hawk_US", "Descriptor_Unit_CH47_Chinook_US"
                M35 = 'Descriptor_Unit_M35_trans_US'
                SMALL_UNIT_TRANSPORTS = [M998_HUMVEE, M998_HUMVEE_M2HB, M998_HUMVEE_AGL, BLACKHAWK]
                LARGE_UNIT_TRANSPORTS = [M1038_HUMVEE, BLACKHAWK]
                HEAVY_TRANSPORTS = [M35, CHINOOK]
                """ TNK """
                # XM4 SLAMMER
                # XM4 SLAMMER AGL
                # RDF/LT
                division_units._register_modded(script.units.TNK.m966_humvee_tow.create(mod_context))
                division_units._register_vanilla('M1025_Humvee_TOW_US', 3)
                division_units._register_modded(units.m998_humvee_glhl.create(mod_context))
                # M1025 HUMVEE AGL
                # transports don't get registered separately
                # M1025 HUMVEE MP
                units.m998_humvee_m2hb.create(mod_context)
                units.m998_humvee_agl.create(mod_context)
                """ REC """
                REC_HUMVEE_M2HB, REC_HUMVEE_AGL = "Descriptor_Unit_M1025_Humvee_scout_US", "Descriptor_Unit_M1025_Humvee_AGL_nonPara_US"
                SMALL_RECON_TRANSPORTS = [M998_HUMVEE, REC_HUMVEE_M2HB, REC_HUMVEE_AGL, BLACKHAWK]
                FAV = script.units.REC.fav.create(mod_context).unit.descriptor_name
                division_units._register_modded(units.fav_agl.create)
                division_units._register_modded(units.fav_m2hb.create)
                # 👓 FAV TOW
                division_units._register_modded(units.folt.create(mod_context), [FAV, REC_HUMVEE_AGL, BLACKHAWK])
                division_units._register_vanilla("LRRP_US", 2, [M998_HUMVEE, "Descriptor_Unit_M151A2_scout_US"])
                # CEWI?
                # KLR-250?
                # M998 HUMVEE G/VLLD
                division_units._register_modded(units.operational_support.create(mod_context), HEAVY_TRANSPORTS)
                division_units._register_modded(units.iew_team.create(mod_context), SMALL_RECON_TRANSPORTS)
                division_units._register_modded(script.units.REC.mot_scouts.create(mod_context), SMALL_RECON_TRANSPORTS)
                division_units._register_modded(script.units.REC.scoutat_team.create(mod_context), SMALL_RECON_TRANSPORTS)
                division_units._register_vanilla("OH58C_Scout_US", 1)
                division_units._register_vanilla("OH58D_Combat_Scout_US", 1)
                division_units._register_vanilla("EH60A_EW_US", 1)
                division_units._register_modded(script.units.HEL.joh58d_kiowa.create(mod_context))
                division_units._register_modded(units.mqm10_aquila.create(mod_context))
                # [[👓]] F-14D TOMCAT TARPS
                """ AA """
                # JOH-58C KIOWA
                division_units._register_modded(script.units.AA.m167a2_pivads_20mm.create(mod_context), [M998_HUMVEE, CHINOOK])
                # EXCALIBUR VWC
                division_units._register_modded(script.units.AA.m998_avenger.create(mod_context))
                # M998 SETTER?
                division_units._register_modded(script.units.AA.xm85_t_chaparral.create(mod_context), [M35])
                division_units._register_vanilla("MANPAD_Stinger_C_US", 1, [M998_HUMVEE, M998_HUMVEE_AGL, BLACKHAWK])
                division_units._register_modded(script.units.AA.stinger_tdar.create(mod_context), [M998_HUMVEE, M998_HUMVEE_M2HB, BLACKHAWK])
                """ HEL """
                division_units._register_vanilla("AH64_Apache_US", 2)
                division_units._register_vanilla("AH64_Apache_emp1_US", 2)
                division_units._register_vanilla("AH64_Apache_ATAS_US", 1)
                division_units._register_modded(script.units.HEL.ah64a_apache_sead.create)
                """ AIR """
                # A-6E INTRUDER [HE]
                # A-6E INTRUDER [CLU]
                # A-6E INTRUDER [LGB]
                # A-6E INTRUDER SWIP
                # EA-6B PROWLER [SEAD]
                # EA-6B PROWLER [EW]
                # A-7E CORSAIR II [HE]
                # A-7E CORSAIR II [SEAD]
                # F-14B TOMCAT [AA1]
                # F-14B TOMCAT [AA2]
                # F-14B TOMCAT [LGB]
            # make division
            division_texture_name: str = mod_context.add_division_emblem(root_msg, "img/patch.png", div_metadata) 
            mod_context.create_division(div_metadata,
                                        "Descriptor_Deck_Division_US_82nd_Airborne_multi",
                                        division_units,
                                        "Descriptor_Deck_Division_US_8th_Inf_multi",
                                        root_msg,
                                        DivisionName=mod_context.localization.register("9TH INFANTRY DIVISION (HTTB)"),
                                        DescriptionHintTitleToken=mod_context.localization.register("9TH INFANTRY DIVISION (HIGH-TECH. TESTBED)"),
                                        EmblemTexture = division_texture_name)
            # add a default deck to Decks.ndf (not required)
    
    generate_mod(mod_metadata, root_msg)
print(f"Generation finished at {datetime.now().time()}")