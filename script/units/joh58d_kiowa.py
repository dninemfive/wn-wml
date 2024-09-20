
from context.mod_creation_context import ModCreationContext
from context.module_context import ModuleContext
from creators.unit import UNIT_UI
from metadata.division_unit_registry import UnitRules
from metadata.unit import UnitMetadata
from ndf_parse.model import List, ListRow, Object
import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
from constants.ndf_paths import WEAPON_DESCRIPTOR, MISSILE_CARRIAGE


def create(ctx: ModCreationContext) -> UnitRules | None:
    # JOH-58D KIOWA
    # like the KIOWA WR. but with 8 TOWs instead of 4 Hellfires
    # maybe use TOW 2A instead of normal TOWs?
    # maybe have 4 TOWs and 19 rockets?
    with ctx.create_unit("#REC2 JOH-58D KIOWA", "US", "OH58D_Combat_Scout_US") as joh58d_kiowa:
        joh58d_kiowa.get_module('WeaponManager', by_name=True).by_member('Default').value = generate_weapon_descriptor(ctx.ndf[WEAPON_DESCRIPTOR])
        joh58d_kiowa.get_module('MissileCarriage', by_name=True).by_member('Default').value = generate_missile_carriages(ctx.ndf[MISSILE_CARRIAGE])
        # insert after Kiowa and before Kiowa WR
        joh58d_kiowa.edit_ui_module(UpgradeFromUnit='Descriptor_Unit_M274_Mule_ITOW_US')
        with ModuleContext(joh58d_kiowa.get_other_unit('M1025_Humvee_TOW_US'), 'TUnitUIModuleDescriptor') as m1025_ui_module:
            m1025_ui_module.edit_members(UpgradeFromUnit='Descriptor_Unit_d9_M966_HUMVEE_TOW_US')
        return UnitRules(joh58d_kiowa, 1, [0, 4, 3, 0])
    
def generate_weapon_descriptor(weapon_descriptor_ndf: List) -> str:
    # copy descriptor
    copy = weapon_descriptor_ndf.by_name('WeaponDescriptor_OH58D_Combat_Scout_US').value.copy()
    # set ammo
    edit.members(copy, Salves=[1,1,])
    # copy first turret unit descriptor from Kiowa WR; replace ammunition with TOW 2A x4
    # copy second turret unit descriptor from Combat Scout; replace ammunition with Hydra 70mm x19
    return '$/GFX/Weapon/WeaponDescriptor_d9_M966_Humvee_TOW_US'

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
    missile_carriage_ndf.add(showroom_copy, namespace='MissileCarriage_d9_JOH58D_KIOWA_US_Showroom')
    return 