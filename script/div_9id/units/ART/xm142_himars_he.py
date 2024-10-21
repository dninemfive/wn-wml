import mw2.utils.ndf.edit as edit
from mw2.context.mod_creation import ModCreationContext
from mw2.context.unit_module import UnitModuleContext
from mw2.creators.ammo import AmmoCreator
from mw2.creators.unit.basic import UNIT_UI
from mw2.creators.weapon import WeaponCreator
from mw2.metadata.unit import UnitMetadata
from mw2.unit_registration.new_src_unit_pair import NewSrcUnitPair
from ndf_parse.model import List, ListRow


def create(ctx: ModCreationContext) -> NewSrcUnitPair:
    # XM142 HIMARS [HE]
    # copy BM-21 Grad
    with ctx.create_unit("XM142 HIMARS [HE]", "US", "BM21_Grad_SOV") as xm142_himars_he:
        # copy MLRS ammo but with 6 instead of 12 shots
        ammo_name = 'Ammo_d9_RocketArt_M26_227mm_HE_x6'
        with ctx.create_ammo(ammo_name, 'Ammo_RocketArt_M26_227mm') as ammo:
            ammo.edit_members(NbTirParSalves=6,
                              AffichageMunitionParSalve=6)
        # change weapon
        with xm142_himars_he.edit_weapons() as weapons:
            edit.members(weapons.get_turret_weapon(0),
                         Ammunition=f'$/GFX/Weapon/{ammo_name}',
                         EffectTag="'FireEffect_RocketArt_M26_227mm'")
        # change nationalite
        xm142_himars_he.modules.type.edit_members(
            Nationalite='Allied',
            MotherCountry='US'
        )
        # update speed, fuel capacity
        # change upgradefromunit, countrytexture
        xm142_himars_he.modules.ui.edit_members(
            UpgradeFromUnit=None,
            CountryTexture='US'
        )
        # change unit dangerousness
        # change unit attack/defense value
        # change unit cost
        return xm142_himars_he
        