from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.division_unit_registry import UnitInfo
from metadata.unit import UnitMetadata
from misc.unit_creator import UNIT_UI
from ndf_parse.model import List, ListRow
from utils.ndf import to_List as qlist

def create(ctx: UnitCreationContext) -> UnitInfo | None:
    # M198 155mm COPPERHEAD
    # copy M198 155mm
    with ctx.create_unit("M198 COPPERHEAD", "US", "Howz_M198_155mm_US") as m198_clu:
        # change ammo type to guided
        # reduce HP by 1
        with m198_clu.module_context('TBaseDamageModuleDescriptor') as damage_module:
            # TODO: dynamically adjust this from M198 
            damage_module.edit_members(MaxPhysicalDamages=7)
        # update transportable (TODO: automate this)
        with m198_clu.module_context('TTransportableModuleDescriptor') as transportable_module:
            transportable_module.edit_members(TransportedSoldier='"d9_M198_COPPERHEAD_US"')
        # upgrade from M198 [CLU]
        with m198_clu.module_context('TUnitUIModuleDescriptor') as ui_module:
            ui_module.edit_members(UpgradeFromUnit="Descriptor_Unit_d9_M198_155mm_CLU_US")
        # change unit dangerousness (see 2S3M1 vs regular)
        # change unit attack/defense value (see 2S3M1 vs regular)
        # change unit cost (see 2S3M1 vs regular)
        return UnitInfo(m198_clu, 2, [0, 4, 3, 0])
        