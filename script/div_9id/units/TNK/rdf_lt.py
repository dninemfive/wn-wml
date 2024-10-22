from mw2.context.mod_creation import ModCreationContext
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair
from ndf_parse.model import List, ListRow, Object


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    with ctx.create_unit("RDF/LT", "US", "AMX_13_90mm_FR") as rdf_lt:
        # TODO: set weapons and armor appropriately
        rdf_lt.modules.ui.UpgradeFromUnit='d9_XM4_SLAMMER_AGL_US'
        return rdf_lt