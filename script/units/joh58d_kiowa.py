
from script.creators import weapon
import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
from constants.ndf_paths import AMMUNITION_MISSILES, MISSILE_CARRIAGE, WEAPON_DESCRIPTOR
from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from creators.weapon import WeaponCreator
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow, Object


def create(ctx: ModCreationContext) -> UnitRules | None:
    # JOH-58D KIOWA
    # like a mix of the other Kiowas, with 4 TOW 2A and 19 Hydra 70
    with ctx.create_unit("#RECO3 JOH-58D KIOWA", "US", "OH58D_Combat_Scout_US") as joh58d_kiowa:
        with joh58d_kiowa.edit_weapons() as weapons:
            edit_weapons(weapons)
        joh58d_kiowa.get_module('MissileCarriage', by_name=True).by_member('Connoisseur').value = generate_missile_carriages(ctx.ndf[MISSILE_CARRIAGE])
        # insert after Kiowa and before Kiowa WR
        joh58d_kiowa.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_OH58D_Combat_Scout_US')
        with ModuleContext(joh58d_kiowa.get_other_unit('OH58D_Kiowa_Warrior_US'), 'TUnitUIModuleDescriptor') as kiowa_wr_ui_module:
            kiowa_wr_ui_module.edit_members(UpgradeFromUnit=joh58d_kiowa.new.descriptor_name)
        return UnitRules(joh58d_kiowa, 1, [0, 4, 3, 0])
    
def generate_ammo_descriptor(ctx: ModCreationContext) -> str:
    ammo_name = 'Ammo_AGM_BGM71D_TOW_2A_x4'
    copy: Object = ctx.ndf[AMMUNITION_MISSILES].by_name('Ammo_ATGM_BGM71D_TOW_2A_x2').value.copy()
    copy.by_member('DescriptorId').value = ctx.guids.generate(ammo_name)
    
def edit_weapons(weapons: WeaponCreator) -> str:
    # set ammo
    weapons.Salves = [1,1]
    # copy first turret unit descriptor from Kiowa WR; replace ammunition with TOW 2A x4
    #       Ammo_AGM_BGM71D_TOW_2_x4
    # TODO: TOW 2A instead?
    turret_weapons: List = weapons.TurretDescriptorList[0].value.by_member('MountedWeaponDescriptorList').value
    turret_weapons[0].value.by_member('Ammunition').value = '$/GFX/Weapon/Ammo_AGM_BGM71D_TOW_2_x4'
    # copy second turret unit descriptor from Combat Scout; replace ammunition with Hydra 70mm x19
    #       Ammo_RocketAir_Hydra_70mm_x19
    weapon_2 = turret_weapons[0].value.copy()
    edit.members(weapon_2,
                 Ammunition='$/GFX/Weapon/Ammo_RocketAir_Hydra_70mm_x19',
                 EffectTag="'FireEffect_RocketAir_Hydra_70mm_x19'",
                 HandheldEquipmentKey="'MeshAlternative_2'",
                 SalvoStockIndex=1,
                 WeaponActiveAndCanShootPropertyName="'WeaponActiveAndCanShoot_2'",
                 WeaponIgnoredPropertyName="'WeaponIgnored_2'",
                 WeaponShootDataPropertyName=['"WeaponShootData_0_2"',])
    turret_weapons.add(ListRow(weapon_2))
    turret_weapons.add(ListRow(make_mounted_weapon(
        weapons,
        
    )))
    weapons.add_mounted_weapon(weapon_index=1,
                               )

def make_mounted_weapon(weapons: WeaponCreator,
                        base: Object | None = None,
                        weapon_index:           int = 0,
                        turret_index:           int = 0,
                        mesh_offset:            int = 1,
                        weapon_shoot_data_ct:   int = 1,
                        **changes) -> Object:
    copy: Object = base.copy() if base is not None else weapons.get_turret_weapon(turret_index, 0)
    mesh_index = weapon_index + mesh_offset
    weapon_shoot_datas = [f'"WeaponShootData_{x}_{mesh_index}"' for x in range(weapon_shoot_data_ct)]
    edit.members(copy,
                 HandheldEquipmentKey=f"'MeshAlternative_{mesh_index}'",
                 SalvoStockIndex=weapon_index,
                 WeaponActiveAndCanShootPropertyName=f"'WeaponActiveAndCanShoot_{mesh_index}'",
                 WeaponIgnoredPropertyName=f"'WeaponIgnored_{mesh_index}'",
                 WeaponShootDataPropertyName=weapon_shoot_datas,
                 **changes)
    return copy

def generate_missile_carriages(missile_carriage_ndf: List) -> str:
    copy: Object = missile_carriage_ndf.by_name('MissileCarriage_OH58D_Combat_Scout_US').value.copy()
    edit.members(copy,
                 WeaponInfos=[
                    ensure._object('TMissileCarriageWeaponInfo', 
                                Count=4,
                                MissileType='eAGM',
                                MountingType='eMountingPod',
                                WeaponIndex='0'),
                    ensure._object('TMissileCarriageWeaponInfo', 
                                Count=19,
                                MissileType='eAGM',
                                MountingType='eMountingPod',
                                WeaponIndex='1')
                ])
    missile_carriage_ndf.add(ListRow(copy, namespace='MissileCarriage_d9_JOH58D_KIOWA_US'))
    showroom_copy = copy.copy()
    edit.members(showroom_copy, PylonSet='~/DepictionPylonSet_Helico_Default_Showroom')
    missile_carriage_ndf.add(value=showroom_copy, namespace='MissileCarriage_d9_JOH58D_KIOWA_US_Showroom')
    return 'MissileCarriage_d9_JOH58D_KIOWA_US'