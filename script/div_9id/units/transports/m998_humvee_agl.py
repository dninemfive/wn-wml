from mw2.context.mod_creation import ModCreationContext
from mw2.creators.unit.basic import BasicUnitCreator
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair
from ndf_parse.model import List, ListRow, MemberRow, Object


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # M998 HUMVEE AGL
    with ctx.create_unit("M998 HUMVEE AGL", "US", "M1025_Humvee_AGL_nonPara_US") as trans_m998_humvee_agl:
        trans_m998_humvee_agl.modules.type.edit_members(
            AcknowUnitType='Transport',
            TypeUnitFormation='Char'
        )
        trans_m998_humvee_agl.tags.add('Vehicule_Transport')
        trans_m998_humvee_agl.tags.remove("Reco", "Radio", "Vehicule_Reco")
        # armed transports (including the MP Humvee) seem to be "appui", or "support"
        # copying such a module from a non-DLC vehicle for compatibility purposes
        trans_m998_humvee_agl.modules.replace_from('BTR_60_DDR', 'TTacticalLabelModuleDescriptor')
        edit_with_m998(trans_m998_humvee_agl, ctx.get_unit("M998_Humvee_US"))
        # apparently all armed transports, even if they have no armor and just a GPMG, go in the TNK tab lol
        trans_m998_humvee_agl.modules.production.edit_members(
            Factory='Tanks',
            command_point_cost = 35
        )
        trans_m998_humvee_agl.modules.ui.edit_members(
            UpgradeFromUnit="d9_M998_HUMVEE_M2HB_US",
            SpecialtiesList=['transport', '_transport1'],
            InfoPanelConfigurationToken='VehiculeTransporter',
            MenuIconTexture='appui',
            TypeStrategicCount='Transport')
        trans_m998_humvee_agl.modules.remove('TDeploymentShiftModuleDescriptor')
        return trans_m998_humvee_agl
    
def edit_with_m998(cmd_m998_humvee_agl: BasicUnitCreator, m998_humvee: Object) -> None:
    # copy scanner from M998 Humvee (regular)
    # if i were making the game i'd give all transports with MGs a slightly better scanner than unarmed ones
    # but that's out of scope for a mod just adding one division
    cmd_m998_humvee_agl.modules.replace_from(m998_humvee, 'TScannerConfigurationDescriptor')
    cmd_m998_humvee_agl.modules.replace_from(m998_humvee, 'TReverseScannerWithIdentificationDescriptor')
    cmd_m998_humvee_agl.modules.replace_from(m998_humvee, 'TVisibilityModuleDescriptor')
    cmd_m998_humvee_agl.modules.replace_from(m998_humvee, 'TFuelModuleDescriptor')