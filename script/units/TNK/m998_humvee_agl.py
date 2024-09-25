import constants.ndf_paths as ndf_paths
from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UnitCreator
from metadata.unit_rules import UnitRules
from ndf_parse.model import List, ListRow, MemberRow, Object
from utils.ndf import ensure
from units._utils import autonomy_to_fuel_move_duration as to_fmd


def create(ctx: ModCreationContext) -> UnitRules | None:
    # M998 HUMVEE AGL
    with ctx.create_unit("M998 HUMVEE AGL", "US", "M1025_Humvee_AGL_nonPara_US") as trans_m998_humvee_agl:
        with trans_m998_humvee_agl.module_context("TTypeUnitModuleDescriptor") as unit_type_module:
            unit_type_module.edit_members(AcknowUnitType="~/TAcknowUnitType_Transport",
                                          TypeUnitFormation="'Char'")
        trans_m998_humvee_agl.add_tags("Vehicule_Transport")
        trans_m998_humvee_agl.remove_tags("Reco", "Radio", "Vehicule_Reco")
        # armed transports (including the MP Humvee) seem to be "appui", or "support"
        # copying such a module from a non-DLC vehicle for compatibility purposes
        trans_m998_humvee_agl.replace_module_from('Descriptor_Unit_BTR_60_DDR', 'TTacticalLabelModuleDescriptor')
        edit_with_m998(trans_m998_humvee_agl, trans_m998_humvee_agl.get_other_unit("M998_Humvee_US"))
        with trans_m998_humvee_agl.module_context('TProductionModuleDescriptor') as production_module:
            # apparently all armed transports, even if they have no armor and just a GPMG, go in the TNK tab lol
            production_module.edit_members(Factory="EDefaultFactories/Tanks", 
                                           ProductionRessourcesNeeded={"$/GFX/Resources/Resource_CommandPoints": 35,
                                                                       "$/GFX/Resources/Resource_Tickets":       1})
        trans_m998_humvee_agl.edit_ui_module(
            UpgradeFromUnit="Descriptor_Unit_d9_M998_HUMVEE_M2HB_US",
            SpecialtiesList=["'transport'", "'_transport1'"],
            InfoPanelConfigurationToken="'VehiculeTransporter'",
            MenuIconTexture="'Texture_RTS_H_appui'",
            TypeStrategicCount='ETypeStrategicDetailedCount/Transport')
        trans_m998_humvee_agl.remove_module('TDeploymentShiftModuleDescriptor')
        return None # transports don't get added separately
    
def edit_with_m998(cmd_m998_humvee_agl: UnitCreator, m998_humvee: Object) -> None:
    # copy scanner from M998 Humvee (regular)
    # if i were making the game i'd give all transports with MGs a slightly better scanner than unarmed ones
    # but that's out of scope for a mod just adding one division
    cmd_m998_humvee_agl.replace_module_from(m998_humvee, 'TScannerConfigurationDescriptor')
    cmd_m998_humvee_agl.replace_module_from(m998_humvee, 'TReverseScannerWithIdentificationDescriptor')
    cmd_m998_humvee_agl.replace_module_from(m998_humvee, 'TVisibilityModuleDescriptor')
    cmd_m998_humvee_agl.replace_module_from(m998_humvee, 'TFuelModuleDescriptor')