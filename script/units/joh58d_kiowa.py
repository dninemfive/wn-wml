
from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow, Object
import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
from constants.ndf_paths import WEAPON_DESCRIPTOR, MISSILE_CARRIAGE, AMMUNITION_MISSILES


def create(ctx: ModCreationContext) -> UnitRules | None:
    # JOH-58D KIOWA
    # like a mix of the other Kiowas, with 4 TOW 2A and 19 Hydra 70
    with ctx.create_unit("#RECO3 JOH-58D KIOWA", "US", "OH58D_Combat_Scout_US") as joh58d_kiowa:
        joh58d_kiowa.get_module('WeaponManager', by_name=True).by_member('Default').value = generate_weapon_descriptor(ctx.ndf[WEAPON_DESCRIPTOR])
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
    
def generate_weapon_descriptor(weapon_descriptor_ndf: List) -> str:
    # copy descriptor
    copy: Object = weapon_descriptor_ndf.by_name('WeaponDescriptor_OH58D_Kiowa_Warrior_US').value.copy()
    # set ammo
    edit.members(copy, Salves=[1,1])
    # copy first turret unit descriptor from Kiowa WR; replace ammunition with TOW 2A x4
    #       Ammo_AGM_BGM71D_TOW_2_x4
    # TODO: TOW 2A instead?
    turret_weapons: List = copy.by_member('TurretDescriptorList').value[0].value.by_member('MountedWeaponDescriptorList').value
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
                 WeaponIgnoredPropertyName="'WeaponIgnored_1'",
                 WeaponShootDataPropertyName=['"WeaponShootData_0_2"',])
    turret_weapons.add(ListRow(weapon_2))
    weapon_descriptor_ndf.add(ListRow(copy, 'export', 'WeaponDescriptor_d9_RECO2_JOH_58D_KIOWA_US'))
    return '$/GFX/Weapon/WeaponDescriptor_d9_RECO2_JOH_58D_KIOWA_US'

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