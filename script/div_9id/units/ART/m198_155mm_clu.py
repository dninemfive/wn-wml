from mw2.context.mod_creation import ModCreationContext
from mw2.context.unit_module import UnitModuleContext
from mw2.metadata.unit import UnitMetadata
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair
import mw2.utils.ndf.ensure as ensure
import mw2.utils.ndf.edit as edit


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # M198 155mm [CLU]
    # copy M198 155mm
    with ctx.create_unit("M198 155mm [CLU]", "US", "Howz_M198_155mm_US") as m198_clu:
        # change ammo type to CLU
        ammo_name = 'Ammo_d9_Howz_Canon_M198_155mm_Cluster'
        with ctx.create_ammo(ammo_name, 'Ammo_Howz_Canon_M198_Howitzer_155mm') as ammo:
            ammo.edit_members(Name=ctx.localization.register('M864 155mm'),
                              TraitsToken=ensure._list("'STAT'", "'cluster'", "'IND'"),
                              Arme=ensure._object('TDamageTypeRTTI', Family='DamageFamily_clu_sol_ap', Index=5),
                              ImpactHappening=["'MortierM240240MmCluster'"],
                              ForceHitTopArmor=True,
                              IsSubAmmunition=True,
                              SupplyCost=160, # TODO: figure out the relative supply cost
                              PiercingWeapon=True)
        with m198_clu.edit_weapons() as weapons:
            edit.members(weapons.get_turret_weapon(0),
                         Ammunition=f'$/GFX/Weapon/{ammo_name}')
        # reduce HP by 1
        m198_clu.modules.base_damage.MaxPhysicalDamages -= 1
        # upgrade from vanilla unit
        m198_clu.modules.ui.UpgradeFromUnit='Howz_M198_155mm_US'
        # change unit dangerousness (see M240 CLU vs regular)
        # change unit attack/defense value (see M240 CLU vs regular)
        # change unit cost (see M240 CLU vs regular) -> about 50% higher
        return m198_clu