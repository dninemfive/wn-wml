from __future__ import annotations

from datetime import datetime
from typing import Callable

import div_9id.ammo
import div_9id.ammo.fgr_17_viper
import div_9id.ammo.m60e3
import div_9id.ammo.m203
import mw2.constants.ndf_paths as ndf_paths
import mw2.constants.paths as paths
from div_9id.units import AA, ART, HEL, INF, LOG, REC, TNK, transports
from mw2.context.mod_creation import ModCreationContext
from mw2.metadata.division import DivisionMetadata
from mw2.metadata.mod import ModMetadata
from mw2.metadata.warno import WarnoMetadata
from mw2.unit_registration.division_unit_registry import DivisionUnitRegistry
from mw2.unit_registration.unit_group import UnitGroup
from mw2.utils.bat import generate_mod, reset_source
from mw2.utils.types.message import Message

wn_metadata = WarnoMetadata(paths.WARNO_DIRECTORY)
mod_metadata = ModMetadata('dninemfive', '9th Infantry Division (Motorized)', wn_metadata, "0.0.0", 'd9', 'd99ID')
div_metadata = DivisionMetadata('d9', '9ID', 'US', 1390)

reset_source(mod_metadata, wn_metadata)

with Message(f"Creating mod {mod_metadata.name} by {mod_metadata.author}") as root_msg:
    with ModCreationContext(mod_metadata, root_msg, *ndf_paths.ALL) as mod_context:
            div_9id.ammo.fgr_17_viper.create(mod_context)
            div_9id.ammo.m60e3.create(mod_context)
            div_9id.ammo.m203.create(mod_context)
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
                                                      "US_101st_Airmobile",
                                                      "UK_2nd_Infantry",
                                                      "FR_11e_Para")
                # make new units              
                # TODO: maybe default unit country?
                # TODO: target module changes with like TModuleType:path/to/property ?      
                transports.init(mod_context)
                for category in [LOG, INF, ART, TNK, REC, AA, HEL]:
                    group: Callable[[DivisionUnitRegistry, Message], UnitGroup] = getattr(category, 'group')
                    group(division_units, msg).register_all()
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