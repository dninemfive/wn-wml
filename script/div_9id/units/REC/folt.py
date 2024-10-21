from mw2.context.mod_creation import ModCreationContext
from ndf_parse.model import List
from ..infantry_weapons import M16A2
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # FOLT
    with ctx.create_infantry_unit("#RECO2 FOLT", "US", "Scout_US", [(M16A2, 2)]) as folt:
        # TODO: GSR trait
        return folt