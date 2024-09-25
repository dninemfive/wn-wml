from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from metadata.unit import UnitMetadata
from metadata.unit_rules import UnitRules
from ndf_parse.model import List, ListRow
from utils.ndf.ensure import _list as qlist


def create(ctx: ModCreationContext) -> UnitRules | None:
    # M167A1 VADS 20mm
    # copy AB version
    with ctx.create_unit("M167A2 PIVADS 20mm", "US", "DCA_M167A2_Vulcan_20mm_Aero_US") as m167a2_pivads:
        # add air-transportable trait
        m167a2_pivads.edit_ui_module(SpecialtiesList=qlist("'AA'", "'_canBeAirlifted'"),
                                     UpgradeFromUnit='Descriptor_Unit_DCA_M167A2_Vulcan_20mm_US')
        # ensure air-transportable with transportation module
        # add "CanBeAirlifted" to tags
        m167a2_pivads.add_tags('"CanBeAirlifted"')
        # advanced: replace soldiers manning it with normal instead of airborne models
        # advanced: insert before AERO-M167A2 PIVADS 20mm
        with ModuleContext(m167a2_pivads.get_other_unit('DCA_M167A2_Vulcan_20mm_Aero_US'), 'TUnitUIModuleDescriptor') as aero_pivads_ui:
            aero_pivads_ui.edit_members(UpgradeFromUnit='Descriptor_Unit_d9_M167A2_PIVADS_20mm_US')
        # update ttransportablemoduledescriptor
        return UnitRules(m167a2_pivads, 2, [0, 4, 3, 0])
        