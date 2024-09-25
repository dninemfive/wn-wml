import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from units._utils import METRE


def create(ctx: ModCreationContext) -> UnitRules | None:
    # M198 155mm COPPERHEAD
    # copy M198 155mm
    with ctx.create_unit("M198 COPPERHEAD", "US", "Howz_M198_155mm_US") as m198_copperhead:
        # change ammo type to guided
        ammo_name = 'Ammo_d9_Howz_Canon_155mm_Copperhead'
        with ctx.create_ammo(ammo_name, 'Ammo_Howz_Canon_M198_Howitzer_155mm') as ammo:
            ammo.edit_members(Name=ctx.localization.register('M712 Copperhead'),
                              TraitsToken=ensure._list("'STAT'", "'cluster'", "'CLGP'"),
                              PorteeMaximaleGRU=17650, # ~ same ratio to the base M198 as the real-life M712 to its counterpart
                              DispersionAtMaxRange=500*METRE,
                              DispersionAtMinRange=500*METRE,
                              CorrectedShotDispersionMultiplier=0.25,
                              CorrectedShotAimtimeMultiplier=0.7,
                              SupplyCost=200, # TODO: figure out the relative supply cost
                             )
        with m198_copperhead.edit_weapons() as weapons:
            edit.members(weapons.get_turret_weapon(0),
                         Ammunition=f'$/GFX/Weapon/{ammo_name}')
        with m198_copperhead.module_context('TBaseDamageModuleDescriptor') as damage_module:
            # TODO: dynamically adjust this from M198 
            damage_module.edit_members(MaxPhysicalDamages=7)
        # upgrade from M198 [CLU]
        with m198_copperhead.module_context('TUnitUIModuleDescriptor') as ui_module:
            ui_module.edit_members(UpgradeFromUnit="Descriptor_Unit_d9_M198_155mm_CLU_US")
        # change unit dangerousness (see 2S3M1 vs regular)
        # change unit attack/defense value (see 2S3M1 vs regular)
        # change unit cost (see 2S3M1 vs regular)
        return UnitRules(m198_copperhead, 2, [0, 4, 3, 0])
        