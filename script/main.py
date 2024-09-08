from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from datetime import datetime
from utils.io import write
from message import Message, try_nest
from misc.import_warno_scripts import import_script
from misc.unit_creator import UnitCreator
from ndf_parse import Mod
from ndf_parse.model import ListRow, Map, MapRow, MemberRow, Object
from utils.bat import generate_mod, reset_source
from utils.ndf import dict_to_map, edit_members, get_module, replace_unit_module
from metadata.division import DivisionMetadata
from metadata.mod import ModMetadata
from metadata.warno import WarnoMetadata
from context.mod_creation_context import ModCreationContext
import ndf_paths as paths
import shutil
import os

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
with Message(f"Creating mod {mod_metadata.name} by {mod_metadata.author}") as root_msg:
    with ModCreationContext(mod_metadata, root_msg, *paths.ALL) as mod_context:
            with root_msg.nest("Creating units") as msg:
                # make new units              
                with UnitCreationContext(mod_context, msg, div_metadata.id * 1000) as units_context:
                    # TODO: target module changes with like TModuleType:path/to/property ?
                    """ LOG """
                    # M998 HUMVEE SUPPLY
                    #   copy of: M35 Supply
                    with units_context.create_unit("M998_Humvee_Supply_US", "M35_supply_US") as m998_humvee_supply:
                         # "UNITE_M35_supply_US" replaced in TTagsModuleDescriptor
                         # ApparenceModel replaced with that of M1038 Humvee
                         # GenericMovement replaced with that of M998 Humvee
                         # LandMovement replaced with that of M998 Humvee
                         # TBaseDamageModuleDescriptor replaced with that of M1038 Humvee
                         # TSupplyModuleDescriptor replaced with that of Rover 101FC Supply
                         # TProductionModuleDescriptor/ProductionResourcesNeeded replaced with that of Rover 101FC Supply
                         with ModuleContext(m998_humvee_supply.unit_object, "TUnitUIModuleDescriptor") as ui_module:
                              # TUnitUIModuleDescriptor/NameToken updated
                              edit_members(ui_module.object, NameToken=f"'{mod_context.register("M998 HUMVEE SUPPLY")}'")
                              # TUnitUIModuleDescriptor/UpgradeFromUnit cleared
                              ui_module.object.remove_by_member("UpgradeFromUnit")
                    # M1075 PLS
                    # copy of: HEMTT
                    with units_context.create_unit("M1075_PLS_US", "HEMTT_US") as m1075_pls:
                        with ModuleContext(m1075_pls.unit_object, "TUnitUIModuleDescriptor") as ui_module:                            
                            edit_members(ui_module.object,
                                        NameToken=f"'{mod_context.register("M1075 PLS")}'",
                                        # TUnitUIModuleDescriptor/UpgradeFromUnit set to M998 HUMVEE SUPPLY
                                        # TODO: add unit registry to units_context and get the descriptor from there
                                        UpgradeFromUnit="Descriptor_Unit_M998_Humvee_Supply_US")
                        # unit rule xp should also be higher
                        pass
                        pack_list[m1075_pls.new.deck_pack_descriptor_path] = 1    
                    # ✪ M998 HUMVEE SGT.
                    # ✪ M1025 HUMVEE AGL
                    # ✪ M1010 TC3V
                    """ INF """
                    # MOT. MP PATROL
                    # (just copy AB MP PATROL)
                    # for MOT. infantry: copy MECH. version, but reduce men to 8 and replace M240B with SAW and LAW with AT-4
                    # ✪ MOT. RIFLES LDR.
                    # MOT. RIFLES (AT-4)
                    with units_context.create_unit("Mot_Rifles_US", "Rifles_US") as mot_rifles:
                         # change number of guys to 8
                         # TODO: figure out appropriate dangerousness, bounding box size, command point cost
                         with ModuleContext(mot_rifles.unit_object, "TBaseDamageModuleDescriptor") as base_damage_module:
                              base_damage_module.edit_members(MaxPhysicalDamages=8)
                         mot_rifles.unit_object.by_member("ModulesDescriptors").value.by_name("WeaponManager").value.by_member("NbSoldatInGroupeCombat").value = 8
                         with ModuleContext(mot_rifles.unit_object, "TTacticalLabelModuleDescriptor") as tactical_label_module:
                              tactical_label_module.edit_members(NbSoldiers=8)
                         with ModuleContext(mot_rifles.unit_object, "TInfantrySquadWeaponAssignmentModuleDescriptor") as weapon_assignment_module:
                              # TODO: simplify this since most squads follow the same general pattern
                              weapon_assignment_module.edit_members(InitialSoldiersToTurretIndexMap=dict_to_map(
                                   {
                                        (
                                             0, [1]
                                        ),
                                        (
                                             1, [1]
                                        ),
                                        {
                                             2, [0]
                                        },
                                        {
                                             3, [0]
                                        },
                                        {
                                             4, [0]
                                        },
                                        {
                                             5, [0]
                                        },
                                        {
                                             6, [0]
                                        },
                                        {
                                             7, [0]
                                        },
                                        {
                                             8, [0, 2]
                                        }
                                   }
                              ))
                         # change M240 to SAW
                         # change LAW to AT4
                         # change TTransportableModuleDescriptor
                         # change UI module
                         with ModuleContext(mot_rifles.unit_object, "TUnitUIModuleDescriptor") as ui_module:
                              ui_module.edit_members(NameToken=f"'{mod_context.register("MOT. RIFLES")}'")
                              # TODO: update from cmd. mot. rifles
                              ui_module.remove_member("UpgradeFromUnit")
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
                    # copy AB M998 AVENGER
                    with units_context.create_unit("M998_Avenger_US", "M998_Avenger_US") as m998_avenger:
                         # remove forward deploy
                         m998_avenger.remove_module("TDeploymentShiftModuleDescriptor")
                         # update UI
                         with ModuleContext(m998_avenger.unit_object, "TUnitUIModuleDescriptor") as ui_module:                            
                            edit_members(ui_module.object,
                                        NameToken=f"'{mod_context.register("M998 AVENGER")}'",
                                        SpecialtiesList=['AA'])
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
            # make division
            # todo: insert this immediately after 8th Infantry Division
            mod_context.create_division(div_metadata,
                                        "Descriptor_Deck_Division_US_82nd_Airborne_multi",
                                        root_msg,
                                        DivisionName=f"'{mod_context.register("9TH INFANTRY DIVISION (MTZ.)")}'",
                                        DescriptionHintTitleToken = f"'{mod_context.register("9TH INFANTRY DIVISION (MOTORIZED)")}'",
                                        EmblemTexture = '"Texture_Division_Emblem_US_35th_infantry_division"',
                                        PackList = dict_to_map(pack_list))
            # add a default deck to Decks.ndf (not required)
    with root_msg.nest("Writing localization") as msg:
        with open(LOCALIZATION_PATH, "w") as file:
             file.write(mod_context.generate_localization_csv())
    generate_mod(mod_metadata, root_msg)
print(f"Generation finished at {datetime.now().time()}")