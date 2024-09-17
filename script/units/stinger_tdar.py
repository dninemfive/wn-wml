from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow

def create(ctx: ModCreationContext) -> UnitRules | None:
    # M198 155mm COPPERHEAD
    # copy M198 155mm
    with ctx.create_unit("STINGER (TDAR)", "US", "MANPAD_Stinger_C_US") as stinger_tdar:
        # update transportable
        with stinger_tdar.module_context('TTransportableModuleDescriptor') as transportable_module:
            transportable_module.edit_members(TransportedSoldier='"d9_STINGER_TDAR_US"')
        # increase air vision
        # from M167A2: 
        #    OpticalStrengthAltitude = 120
        #    SpecializedDetectionsGRU = MAP[(EVisionUnitType/AlwaysInHighAltitude, 10601.0)]
        # TODO: dynamically set this by averaging the Stinger C value with the M167A2 value
        # even more TODO: custom trait which leaves the normal Stinger C value when moving and activates the radar when stationary
        with stinger_tdar.module_context('TScannerConfigurationDescriptor') as scanner_module:
            scanner_module.edit_members(OpticalStrengthAltitude=100, 
                                        SpecializedDetectionsGRU={"EVisionUnitType/AlwaysInHighAltitude": str((8481.0 + 10601.0)/2)})
        # upgrade from AB Stinger C
        with stinger_tdar.module_context('TUnitUIModuleDescriptor') as ui_module:
            ui_module.edit_members(UpgradeFromUnit="Descriptor_Unit_MANPAD_Stinger_C_Aero_US")
        # change unit dangerousness
        # change unit attack/defense value
        # change unit cost
        return UnitRules(stinger_tdar, 2, [0, 4, 3, 0])