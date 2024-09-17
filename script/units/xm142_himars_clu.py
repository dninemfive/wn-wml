from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow
from utils.ndf import to_List as qlist

from creators.ammo import AmmoCreator
from creators.weapon import WeaponCreator


def create(ctx: ModCreationContext) -> UnitRules | None:
    # XM142 HIMARS [CLU]
    # copy BM-21 Grad
    with ctx.create_unit("XM142 HIMARS [CLU]", "US", "BM21_Grad_SOV") as xm142_himars_clu:
        # copy MLRS ammo but with 6 instead of 12 shots
        with AmmoCreator(ctx, "RocketArt_M26_227mm_Cluster_HIMARS") as ammo:
            ammo.edit_members(NbTirParSalves=6,
                              AffichageMunitionParSalve=6)
        test = List
        test.index()
        with WeaponCreator(ctx, xm142_himars_clu.new, "M270_MLRS_cluster_US") as weapon:
            weapon.object.by_member("TurretDescriptorList").value[0]\
                         .by_member("MountedWeaponDescriptorList").value[0]\
                         .by_member("Ammunition").value = "Ammo_d9_RocketArt_M26_227mm_Cluster_HIMARS"
        # change nationalite
        with xm142_himars_clu.module_context("TTypeUnitModuleDescriptor") as unit_type_module:
            unit_type_module.edit_members(Nationalite="ENationalite/Allied",
                                          MotherCountry="'US'")
        # change weapon
        # update speed, fuel capacity
        # change upgradefromunit, countrytexture
        # change unit dangerousness (see 2S3M1 vs regular)
        # change unit attack/defense value (see 2S3M1 vs regular)
        # change unit cost (see 2S3M1 vs regular)
        return UnitRules(xm142_himars_clu, 2, [0, 4, 3, 0])
        