from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair
from ndf_parse.model import List, ListRow


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    with ctx.create_unit("STINGER (TDAR)", "US", "MANPAD_Stinger_C_US") as stinger_tdar:
        # increase air vision
        # from M167A2: 
        #    OpticalStrengthAltitude = 120
        #    SpecializedDetectionsGRU = MAP[(EVisionUnitType/AlwaysInHighAltitude, 10601.0)]
        # TODO: custom trait which leaves the normal Stinger C value when moving and activates the radar (M167A2 value) when stationary
        stinger_tdar.modules.edit_members('TScannerConfigurationDescriptor',
                                          OpticalStrengthAltitude=100,
                                          SpecializedDetectionsGRU={"EVisionUnitType/AlwaysInHighAltitude": str((8481.0 + 10601.0)/2)})
        # upgrade from AB Stinger C
        stinger_tdar.modules.ui.UpgradeFromUnit = 'MANPAD_Stinger_C_Aero_US'
        # change unit dangerousness
        # change unit attack/defense value
        # change unit cost
        return stinger_tdar