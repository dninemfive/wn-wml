from context.mod_creation import ModCreationContext
from context.unit_module import UnitModuleContext
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow

def create(ctx: ModCreationContext) -> UnitRules | None:
    # M198 155mm COPPERHEAD
    # copy M198 155mm
    with ctx.create_unit("STINGER (TDAR)", "US", "MANPAD_Stinger_C_US") as stinger_tdar:
        # increase air vision
        # from M167A2: 
        #    OpticalStrengthAltitude = 120
        #    SpecializedDetectionsGRU = MAP[(EVisionUnitType/AlwaysInHighAltitude, 10601.0)]
        # TODO: dynamically set this by averaging the Stinger C value with the M167A2 value
        # even more TODO: custom trait which leaves the normal Stinger C value when moving and activates the radar when stationary
        stinger_tdar.modules.edit_members('TScannerConfigurationDescriptor',
                                          OpticalStrengthAltitude=100,
                                          SpecializedDetectionsGRU={"EVisionUnitType/AlwaysInHighAltitude": str((8481.0 + 10601.0)/2)})
        # upgrade from AB Stinger C
        stinger_tdar.modules.ui.UpgradeFromUnit = 'MANPAD_Stinger_C_Aero_US'
        # change unit dangerousness
        # change unit attack/defense value
        # change unit cost
        return UnitRules(stinger_tdar, 2, [0, 4, 3, 0])