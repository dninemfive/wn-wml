import constants.ndf_paths as ndf_paths
from context.mod_creation import ModCreationContext
from context.unit_module import UnitModuleContext
from creators.unit.basic import BasicUnitCreator
from metadata.unit_rules import UnitRules
from ndf_parse.model import List, ListRow, MemberRow, Object
from units._utils import autonomy_to_fuel_move_duration as to_fmd
from utils.ndf import ensure


def create(ctx: ModCreationContext) -> UnitRules | None:
    # ✪ M998 HUMVEE AGL
    with ctx.create_unit("#CMD M998 HUMVEE AGL", "US", "M1025_Humvee_AGL_US") as cmd_m998_humvee_agl:
        cmd_m998_humvee_agl.modules.edit_members('TTypeUnitModuleDescriptor',
                                                 AcknowUnitType="~/TAcknowUnitType_Command",
                                                 TypeUnitFormation="'Supply'")
        cmd_m998_humvee_agl.unit.modules.edit_members('TTypeUnitModuleDescriptor',
                                                      AcknowUnitType="~/TAcknowUnitType_Command",
                                                      TypeUnitFormation="'Supply'")
        cmd_m998_humvee_agl.modules.tags.add("AllowedForMissileRoE", "Commandant", "InfmapCommander", "Vehicule_CMD")
        cmd_m998_humvee_agl.modules.tags.remove("Reco", "Vehicule_Reco", "Vehicule_Transport_Arme")
        # add command module
        cmd_m998_humvee_agl.modules.append(ListRow(Object('TCommanderModuleDescriptor')))
        edit_with_vbl_pc(cmd_m998_humvee_agl, ctx.get_unit("VBL_PC_FR"))
        edit_with_m1025(cmd_m998_humvee_agl, ctx.get_unit("M1025_Humvee_CMD_US"))
        cmd_m998_humvee_agl.modules.remove('Transporter', by_name=True)
        cmd_m998_humvee_agl.modules.production.command_point_cost = 85
        cmd_m998_humvee_agl.modules.production.Factory = 'Logistic'
        cmd_m998_humvee_agl.modules.append(Object('TInfluenceScoutModuleDescriptor'))
        cmd_m998_humvee_agl.modules.ui.UpgradeFromUnit='M1025_Humvee_CMD_para_US'
        cmd_m998_humvee_agl.modules.append(Object('TInfluenceScoutModuleDescriptor'))
        cmd_m998_humvee_agl.modules.ui.edit_members(
            UpgradeFromUnit='M1025_Humvee_CMD_para_US',
            UnitRole="'tank_B'",
            SpecialtiesList=["'hq_veh'", "'_leader'"],
            InfoPanelConfigurationToken="'Default'",
            MenuIconTexture="'Texture_RTS_H_CMD_veh'",
            TypeStrategicCount='ETypeStrategicDetailedCount/CMD_Veh')
        cmd_m998_humvee_agl.modules.remove('TDeploymentShiftModuleDescriptor')
        return UnitRules(cmd_m998_humvee_agl, 1, [0, 3, 2, 0])
    
def edit_with_vbl_pc(cmd_m998_humvee_agl: BasicUnitCreator, vbl_pc: Object) -> None:
    # replace orderavailability with VBL PC (since that's an _armed_ command unit)                                       
    cmd_m998_humvee_agl.modules.replace_from(vbl_pc, 'TCubeActionModuleDescriptor')
    cmd_m998_humvee_agl.modules.replace_from(vbl_pc, 'TOrderConfigModuleDescriptor')
    cmd_m998_humvee_agl.modules.replace_from(vbl_pc, 'TOrderableModuleDescriptor')
    
def edit_with_m1025(cmd_m998_humvee_agl: BasicUnitCreator, m1025_cmd: Object) -> None:
    # scanner from M1025 CMD
    cmd_m998_humvee_agl.modules.replace_from(m1025_cmd, 'TScannerConfigurationDescriptor')
    cmd_m998_humvee_agl.modules.replace_from(m1025_cmd, 'TemplateUnitCriticalModule')
    cmd_m998_humvee_agl.modules.replace_from(m1025_cmd, 'TReverseScannerWithIdentificationDescriptor')
    cmd_m998_humvee_agl.modules.replace_from(m1025_cmd, 'TTacticalLabelModuleDescriptor')
    cmd_m998_humvee_agl.modules.append_from(m1025_cmd, 'TZoneInfluenceMapModuleDescriptor')
    # change stealth to Mediocre (same as M1025 Humvee CP)
    cmd_m998_humvee_agl.modules.append_from(m1025_cmd, 'TVisibilityModuleDescriptor')
    # change autonomy to 36/61 (same as M1025 Humvee CP)
    cmd_m998_humvee_agl.modules.append_from(m1025_cmd, 'TFuelModuleDescriptor')