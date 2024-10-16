import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
import utils.ndf.unit_module as module
from context.mod_creation import ModCreationContext
from context.unit_module import UnitModuleContext
from creators.unit.basic import UNIT_UI
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow


def create(ctx: ModCreationContext) -> UnitRules | None:
    # 👓 FAV AGL
    # model: ILTIS MILAN
    #   replace turret model with AGL
    # range: custom
    # air transportable
    # stealth, vision: M151A2 M2HB
    # weapon: Mk.19 Mod III 40mm, SAW
    with ctx.create_unit("#RECO1 FAV", "US", "Iltis_trans_RFA") as fav:
        fav.modules.type.edit_members(
            AcknowUnitType='Reco',
            TypeUnitFormation='Reconnaissance',
            MotherCountry='US'                             # TODO: set this, icon flag, &c with one item
        )
        fav.modules.production.Factory = 'Recons'
        fav.tags.add('Vehicule_Reco')
        fav.modules.ui.edit_members(
            SpecialtiesList=['reco', '_transport1', 'air_transportable'],
            MenuIconTexture='RECO_veh',
            TypeStrategicCount='Reco_Veh'
        )
        # stealth, vision: M151A2 M2HB
        m151a2_scout = ctx.get_unit('M151A2_scout_US')
        fav.modules.replace_from(m151a2_scout, 'TVisibilityModuleDescriptor')
        fav.modules.replace_from(m151a2_scout, 'TScannerConfigurationDescriptor')
        fav.modules.replace_from(m151a2_scout, 'TReverseScannerWithIdentificationDescriptor')
        fav.modules.replace_from(m151a2_scout, 'TTacticalLabelModuleDescriptor')
        fav.modules.append_from( m151a2_scout, 'TDeploymentShiftModuleDescriptor')
        fav.modules.remove('Transporter', by_name=True)
        return UnitRules(fav, 2, [0, 4, 3, 0])