from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # XM119 IMCS
    # copy VLRA mortar
    with ctx.create_unit("XM1100 120mm", "US", "VLRA_Mortier81_FR") as xm1100_120mm:
        xm1100_120mm.modules.ui.edit_members(
            SpecialtiesList=['mortar'],
            UpgradeFromUnit='Mortier_107mm_US',
            CountryTexture='US'
        )
        # change main weapon to a somewhat improved version of the M30 (or maybe the Tampella?)
        # change country (+flag) to US
        xm1100_120mm.modules.type.MotherCountry = 'US'
        xm1100_120mm.modules.remove('TDeploymentShiftModuleDescriptor')
        return xm1100_120mm
        