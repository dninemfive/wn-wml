from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair
from ndf_parse.model import List, ListRow, Object


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # like the vanilla version but not a recon unit, more comparable to Soviet support AGL vehicles
    with ctx.create_unit("M1025 HUMVEE AGL", "US", "M1025_Humvee_AGL_US") as m1025_agl:
        m1025_agl.modules.type.AcknowUnitType = 'Vehicle'
        m1025_agl.modules.type.TypeUnitFormation = 'Char'
        m1025_agl.modules.ui.UpgradeFromUnit=None
        m1025_agl.modules.ui.SpecialtiesList=['appui']
        m1025_agl.modules.ui.MenuIconTexture = 'appui'
        m1025_agl.modules.ui.TypeStrategicCount = 'Support'
        m1025_agl.modules.remove('TDeploymentShiftModuleDescriptor')
        m1025_agl.modules.remove('Transporter', by_name=True)
        return m1025_agl