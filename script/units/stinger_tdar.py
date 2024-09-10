from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.division_unit_registry import UnitInfo
from metadata.unit import UnitMetadata
from misc.unit_creator import UNIT_UI
from ndf_parse.model import List, ListRow
from utils.ndf import to_List as qlist
from utils.ndf import map_from_tuples

def create(ctx: UnitCreationContext) -> UnitInfo | None:
    # M198 155mm COPPERHEAD
    # copy M198 155mm
    with ctx.create_unit("STINGER (TDAR)", "US", "MANPAD_Stinger_C_US") as stinger_tdar:
        # update transportable (TODO: automate this)
        with stinger_tdar.module_context('TTransportableModuleDescriptor') as transportable_module:
            transportable_module.edit_members(TransportedSoldier='"d9_STINGER_TDAR_US"')
        # increase air vision
        # from M167A2: 
        #    OpticalStrengthAltitude = 120
        #    SpecializedDetectionsGRU = MAP[(EVisionUnitType/AlwaysInHighAltitude, 10601.0)]
        # TODO: dynamically set this by averaging the Stinger C value with the M167A2 value
        with stinger_tdar.module_context('TScannerConfigurationDescriptor') as scanner_module:
            scanner_module.edit_members(OpticalStrengthAltitude=100, 
                                        SpecializedDetectionsGRU=map_from_tuples(("EVisionUnitType/AlwaysInHighAltitude",
                                                                                 str((8481.0 + 10601.0)/2))))
        # upgrade from AB Stinger C
        with stinger_tdar.module_context('TUnitUIModuleDescriptor') as ui_module:
            ui_module.edit_members(UpgradeFromUnit="Descriptor_Unit_MANPAD_Stinger_C_Aero_US")
        # change unit dangerousness
        # change unit attack/defense value
        # change unit cost
        return UnitInfo(stinger_tdar, 2, [0, 4, 3, 0])