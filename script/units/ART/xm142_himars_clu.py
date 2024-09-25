import utils.ndf.edit as edit
from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.ammo import AmmoCreator
from creators.unit import UNIT_UI
from creators.weapon import WeaponCreator
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow


def create(ctx: ModCreationContext) -> UnitRules | None:
    # XM142 HIMARS [CLU]
    # copy BM-21 Grad
    with ctx.create_unit("XM142 HIMARS [CLU]", "US", "BM21_Grad_SOV") as xm142_himars_clu:
        # copy MLRS ammo but with 6 instead of 12 shots
        ammo_name = 'Ammo_d9_RocketArt_M26_227mm_Cluster_x6'
        with ctx.create_ammo(ammo_name, 'Ammo_RocketArt_M26_227mm_Cluster') as ammo:
            ammo.edit_members(NbTirParSalves=6,
                              AffichageMunitionParSalve=6)
        # change weapon
        with xm142_himars_clu.edit_weapons() as weapons:
            edit.members(weapons.get_turret_weapon(0),
                         Ammunition=f'$/GFX/Weapon/{ammo_name}',
                         EffectTag="'FireEffect_RocketArt_M26_227mm_Cluster'")
        # change nationalite
        with xm142_himars_clu.module_context("TTypeUnitModuleDescriptor") as unit_type_module:
            unit_type_module.edit_members(Nationalite="ENationalite/Allied",
                                          MotherCountry="'US'")
        # update speed, fuel capacity
        # change upgradefromunit, countrytexture
        with xm142_himars_clu.module_context('TUnitUIModuleDescriptor') as ui_module:
            # ui_module.remove_member('UpgradeFromUnit')
            ui_module.edit_members(CountryTexture="'CommonTexture_MotherCountryFlag_US'", UpgradeFromUnit='Descriptor_Unit_d9_XM142_HIMARS_HE_US')
        # change unit dangerousness
        # change unit attack/defense value
        # change unit cost
        return UnitRules(xm142_himars_clu, 2, [0, 4, 3, 0])
        