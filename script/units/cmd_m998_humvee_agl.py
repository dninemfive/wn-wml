import constants.ndf_paths as ndf_paths
from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UnitCreator
from metadata.unit_rules import UnitRules
from ndf_parse.model import List, ListRow, MemberRow, Object
from utils.ndf import ensure
from units._utils import autonomy_to_fuel_move_duration as to_fmd


def create(ctx: ModCreationContext) -> UnitRules | None:
    # ✪ M998 HUMVEE AGL
    with ctx.create_unit("#CMD M998 HUMVEE AGL", "US", "M1025_Humvee_AGL_US") as cmd_m998_humvee_agl:
        # acknow type = cmd
        with cmd_m998_humvee_agl.module_context("TTypeUnitModuleDescriptor") as unit_type_module:
            unit_type_module.edit_members(AcknowUnitType="~/TAcknowUnitType_Command",
                                          TypeUnitFormation="'Supply'")
        cmd_m998_humvee_agl.add_tags("AllowedForMissileRoE", "Commandant", "InfmapCommander", "Vehicule_CMD")
        cmd_m998_humvee_agl.remove_tags("Reco", "Vehicule_Reco", "Vehicule_Transport_Arme")
        # add command module
        cmd_m998_humvee_agl.append_module(ListRow(Object('TCommanderModuleDescriptor')))
        edit_with_vbl_pc(cmd_m998_humvee_agl, cmd_m998_humvee_agl.get_other_unit("VBL_PC_FR"))
        edit_with_m1025(cmd_m998_humvee_agl, cmd_m998_humvee_agl.get_other_unit("M1025_Humvee_CMD_US"))
        cmd_m998_humvee_agl.remove_module('Transporter', by_name=True)
        with cmd_m998_humvee_agl.module_context('TProductionModuleDescriptor') as production_module:
            production_module.edit_members(Factory="EDefaultFactories/Logistic", 
                                           ProductionRessourcesNeeded={"$/GFX/Resources/Resource_CommandPoints": str(85),
                                                                       "$/GFX/Resources/Resource_Tickets":       str(1)})        
        cmd_m998_humvee_agl.append_module(Object('TInfluenceScoutModuleDescriptor'))
        cmd_m998_humvee_agl.edit_ui_module(
            UpgradeFromUnit="Descriptor_Unit_M1025_Humvee_CMD_para_US",
            UnitRole="'tank_B'",
            SpecialtiesList=["'hq_veh'", "'_leader'"],
            InfoPanelConfigurationToken="'Default'",
            MenuIconTexture="'Texture_RTS_H_CMD_veh'",
            TypeStrategicCount='ETypeStrategicDetailedCount/CMD_Veh')
        cmd_m998_humvee_agl.remove_module('TDeploymentShiftModuleDescriptor')
        return UnitRules(cmd_m998_humvee_agl, 1, [0, 3, 2, 0])
    
def edit_with_vbl_pc(cmd_m998_humvee_agl: UnitCreator, vbl_pc: Object) -> None:
    # replace orderavailability with VBL PC (since that's an _armed_ command unit)                                       
    cmd_m998_humvee_agl.replace_module_from(vbl_pc, 'TCubeActionModuleDescriptor')
    cmd_m998_humvee_agl.replace_module_from(vbl_pc, 'TOrderConfigModuleDescriptor')
    cmd_m998_humvee_agl.replace_module_from(vbl_pc, 'TOrderableModuleDescriptor')
    
def edit_with_m1025(cmd_m998_humvee_agl: UnitCreator, m1025_cmd: Object) -> None:
    # scanner from M1025 CMD
    cmd_m998_humvee_agl.replace_module_from(m1025_cmd, 'TScannerConfigurationDescriptor')
    cmd_m998_humvee_agl.replace_module_from(m1025_cmd, 'TemplateUnitCriticalModule')
    cmd_m998_humvee_agl.replace_module_from(m1025_cmd, 'TReverseScannerWithIdentificationDescriptor')
    cmd_m998_humvee_agl.replace_module_from(m1025_cmd, 'TTacticalLabelModuleDescriptor')
    cmd_m998_humvee_agl.append_module_from(m1025_cmd, 'TZoneInfluenceMapModuleDescriptor')
    # change stealth to Mediocre (same as M1025 Humvee CP)
    cmd_m998_humvee_agl.append_module_from(m1025_cmd, 'TVisibilityModuleDescriptor')
    # change autonomy to 36/61 (same as M1025 Humvee CP)
    cmd_m998_humvee_agl.append_module_from(m1025_cmd, 'TFuelModuleDescriptor')