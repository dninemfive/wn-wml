import utils.ndf.ensure as ensure
from context.mod_creation import ModCreationContext
from context.unit_module import UnitModuleContext
from metadata.division_unit_registry import UnitRules


def create(ctx: ModCreationContext) -> UnitRules | None:
    with ctx.create_unit("AH-64A APACHE [SEAD]", "US", "AH64_Apache_ATAS_US") as apache_sead:
        # upgrade from Apache ATAS or whatever is at the end of the apache upgrades list
        # new depiction?
        # new weapondescriptor
        # new MissileCarriage
        # same one for both in-game and showroom
        missile_carriage = ensure._object('TMissileCarriageConnoisseur',
            MeshDescriptor='$/GFX/DepictionResources/Modele_AH64_Apache_ATAS_US',
            PylonSet='~/DepictionPylonSet_Helico_Default',
            WeaponInfos=[
                ensure._object('TMissileCarriageWeaponInfo',
                               Count=2,
                               MissileType='eAGM',
                               WeaponIndex=2),
                ensure._object('TMissileCarriageWeaponInfo',
                               Count=8,
                               MissileType='eAGM',
                               WeaponIndex=2)                               
            ]
        )
        # new missilecarriagedepiction
        # maybe use the ATGM Apache model and do MissileCount=1 ProjectileModelResource=AIM-9 or smth?
        # note to self: make sure to set custom cadavre in addition to custom showroom unit
        apache_sead.modules.production.command_point_cost = 250
        apache_sead.modules.ui.SpecialtiesList = ['sead']
        return UnitRules(apache_sead, 1, [0, 3, 2, 0])