from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow
import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
import utils.ndf.unit_module as module


def create(ctx: ModCreationContext) -> UnitRules | None:
    # 👓 FAV
    with ctx.create_unit("#RECO1 FAV", "US", "Iltis_trans_RFA") as fav:
        with fav.module_context('TTypeUnitModuleDescriptor') as type_module:
            type_module.edit_members(AcknowUnitType='~/TAcknowUnitType_Reco',
                                     TypeUnitFormation="'Reconnaissance'")
        fav.MotherCountry = 'US'
        fav.Factory = 'Recons'
        fav.add_tag('Vehicule_Reco')
        # transport, _transport_1, air_transportable
        fav.edit_ui_module(SpecialtiesList=["'reco'", "'_transport1'", "'air_transportable'"],
                           MenuIconTexture="'Texture_RTS_H_RECO_veh'",
                           TypeStrategicCount='ETypeStrategicDetailedCount/Reco_Veh')
        # stealth, vision: M151A2 M2HB
        m151a2_scout = fav.get_other_unit('M151A2_scout_US')
        fav.replace_module_from(m151a2_scout, 'TVisibilityModuleDescriptor')
        fav.replace_module_from(m151a2_scout, 'TScannerConfigurationDescriptor')
        fav.replace_module_from(m151a2_scout, 'TReverseScannerWithIdentificationDescriptor')
        fav.replace_module_from(m151a2_scout, 'TTacticalLabelModuleDescriptor')
        fav.append_module_from( m151a2_scout, 'TDeploymentShiftModuleDescriptor')
        # add a little bit of ECM to represent being a very small target?
        return UnitRules(fav, 2, [0, 4, 3, 0])