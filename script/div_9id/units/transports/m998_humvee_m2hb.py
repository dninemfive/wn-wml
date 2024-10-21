from mw2.context.mod_creation import ModCreationContext
from mw2.creators.unit.basic import BasicUnitCreator
from ndf_parse.model import List, ListRow, MemberRow, Object
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # M998 HUMVEE M2HB
    with ctx.create_unit("M998 HUMVEE M2HB", "US", "M1025_Humvee_scout_US") as trans_m998_humvee_m2hb:
        trans_m998_humvee_m2hb.modules.type.edit_members(
            AcknowUnitType="Transport",
            TypeUnitFormation='Char'
        )
        trans_m998_humvee_m2hb.modules.tags.add("Vehicule_Transport")
        trans_m998_humvee_m2hb.modules.tags.remove("Reco", "Radio", "Vehicule_Reco")
        # armed transports (including the MP Humvee) seem to be "appui", or "support"
        # copying such a module from a non-DLC vehicle for compatibility purposes
        trans_m998_humvee_m2hb.modules.replace_from('Descriptor_Unit_BTR_60_DDR', 'TTacticalLabelModuleDescriptor')
        edit_with_m998(trans_m998_humvee_m2hb, ctx.get_unit("M998_Humvee_US"))
        trans_m998_humvee_m2hb.modules.production.edit_members(
            # apparently all armed transports, even if they have no armor and just a GPMG, go in the TNK tab lol
            Factory='Tanks',
            command_point_cost=35
        )
        trans_m998_humvee_m2hb.modules.ui.edit_members(
            UpgradeFromUnit="M1025_Humvee_MP_US",
            SpecialtiesList=['transport', '_transport1'], # TODO: function to set something as a transporter or a prime mover all in one go
            InfoPanelConfigurationToken='VehiculeTransporter',
            MenuIconTexture='appui',
            TypeStrategicCount='Transport')
        trans_m998_humvee_m2hb.modules.remove('TDeploymentShiftModuleDescriptor')
        return None # transports don't get added separately
    
def edit_with_m998(trans_m998_humvee_m2hb: BasicUnitCreator, m998_humvee: Object) -> None:
    # copy scanner from M998 Humvee (regular)
    # if i were making the game i'd give all transports with MGs a slightly better scanner than unarmed ones
    # but that's out of scope for a mod just adding one division
    trans_m998_humvee_m2hb.modules.replace_from(m998_humvee, 'TScannerConfigurationDescriptor')
    trans_m998_humvee_m2hb.modules.replace_from(m998_humvee, 'TReverseScannerWithIdentificationDescriptor')
    trans_m998_humvee_m2hb.modules.replace_from(m998_humvee, 'TVisibilityModuleDescriptor')
    trans_m998_humvee_m2hb.modules.replace_from(m998_humvee, 'TFuelModuleDescriptor')