from context.module_context import ModuleContext
from context.unit_creation_context import UnitCreationContext
from metadata.division_unit_registry import UnitInfo
from metadata.unit import UnitMetadata
from misc.unit_creator import UNIT_UI
from misc.ammo_creator import AmmoCreator
from misc.weapon_creator import WeaponCreator
from ndf_parse.model import List, ListRow
from utils.ndf import to_List as qlist

def create(ctx: UnitCreationContext) -> UnitInfo | None:
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
        return UnitInfo(xm142_himars_clu, 2, [0, 4, 3, 0])
        