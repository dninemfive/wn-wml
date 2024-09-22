# right, python is stupid so i can't use type hints for this
# from context.unit_creation_context import UnitCreationContext
from typing import Callable, Self

import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
from constants.ndf_paths import WEAPON_DESCRIPTOR
from context.module_context import ModuleContext
from metadata.unit import UnitMetadata
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue
from utils.ndf.decorators import ndf_path
from utils.types.message import Message, try_nest


class WeaponCreator(object):
    def __init__(self: Self, ndf: dict[str, List], unit: UnitMetadata, copy_of: str, parent_msg: Message | None = None, callback: Callable[[str], None] = None):
        self.ndf = ndf
        self.name = ensure.prefix(unit.name, 'WeaponDescriptor_')
        self.copy_of = ensure.prefix(copy_of, 'WeaponDescriptor_')
        self.parent_msg = parent_msg
        self.callback = callback

    def __enter__(self: Self) -> Self:
        self.msg = try_nest(self.parent_msg, f"Creating {self.name}")
        self.msg.__enter__()
        with self.msg.nest(f"Copying {self.copy_of}") as _:
            self.object = self.make_copy()
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        self.apply()
        self.callback(self.name)
        self.msg.__exit__(exc_type, exc_value, traceback)

    def apply(self: Self):
        with self.msg.nest(f"Saving {self.name}") as msg2:
            self.edit_ammunition(self.ndf, msg2)

    def make_copy(self: Self) -> Object:
        copy: Object = self.ndf[WEAPON_DESCRIPTOR].by_name(self.copy_of).value.copy()
        return copy

    @ndf_path(WEAPON_DESCRIPTOR)
    def edit_ammunition(self: Self, ndf: List):
        ndf.add(ListRow(self.object, namespace=self.name, visibility="export"))

    def edit_members(self: Self, **kwargs: CellValue):
        edit.members(self.object, **kwargs)

    @property
    def Salves(self: Self) -> List:
        return self.object.by_member('Salves').value
    
    @Salves.setter
    def Salves(self: Self, value: list[int] | List) -> None:
        self.edit_members(Salves=value)

    @property
    def SalvoIsMainSalvo(self: Self) -> List | None:
        try:
            return self.object.by_member('SalvoIsMainSalvo').value
        except:
            return None
        
    @SalvoIsMainSalvo.setter
    def SalvoIsMainSalvo(self: Self, value: list[bool] | List) -> None:
        self.edit_members(SalvoIsMainSalvo=value)

    @property
    def AlwaysOrientArmorTowardsThreat(self: Self) -> bool:
        return bool(self.object.by_member("AlwaysOrientArmorTowardsThreat").value)
    
    @AlwaysOrientArmorTowardsThreat.setter
    def AlwaysOrientArmorTowardsThreat(self: Self, value: str | bool) -> None:
        self.edit_members(AlwaysOrientArmorTowardsThreat=value)

    @property
    def TurretDescriptorList(self: Self) -> List:
        return self.object.by_member('TurretDescriptorList').value
    
    # @TurretDescriptorList.setter
    # def TurretDescriptorList(self: Self, value: list[Object] | List) -> None:
    #    self.edit_members(TurretDescriptorList=value)

    def get_turret_weapon_list(self: Self, turret_or_turret_index: Object | ListRow | int) -> List:
        turret: Object = ensure.notrow(self.TurretDescriptorList[turret_or_turret_index]
                                       if isinstance(turret_or_turret_index, int)
                                       else turret_or_turret_index)
        return turret.by_member('MountedWeaponDescriptorList').value

    def get_turret_weapon(self: Self, turret_or_weapon_index: int, weapon_index_in_turret: int | None = None) -> Object:
        if weapon_index_in_turret is None:
            weapon_index_in_turret = turret_or_weapon_index
            turret_or_weapon_index = 0
        return self.get_turret_weapon_list(turret_or_weapon_index)[weapon_index_in_turret].value
    
    def get_weapon_counts(self: Self) -> list[list[int]]:
        result = []
        weapon_index: int = 0
        for turret in self.TurretDescriptorList:
            turret_data: list[int] = []
            for _ in self.get_turret_weapon_list(turret):
                turret_data.append(weapon_index)
                weapon_index += 1
            result.append(turret_data)
        return result
    
    def next_weapon_index(self: Self) -> int:
        result: int = -1
        for l in self.get_weapon_counts():
            for i in l:
                result = max(result, i)
        return result + 1
    
    def add_mounted_weapon(self: Self,
                        base: Object | None = None,
                        turret_index:           int = 0,
                        weapon_index:           int | None = None,
                        mesh_offset:            int = 1,
                        weapon_shoot_data_ct:   int = 1,
                        **changes) -> None:
        if weapon_index is None:
            weapon_index = self.next_weapon_index()
        copy: Object = base.copy() if base is not None else self.get_turret_weapon(turret_index, 0).copy()
        mesh_index = weapon_index + mesh_offset
        weapon_shoot_datas = [f'"WeaponShootData_{x}_{mesh_index}"' for x in range(weapon_shoot_data_ct)]
        edit.members(copy,
                    HandheldEquipmentKey=f"'MeshAlternative_{mesh_index}'",
                    SalvoStockIndex=weapon_index,
                    WeaponActiveAndCanShootPropertyName=f"'WeaponActiveAndCanShoot_{mesh_index}'",
                    WeaponIgnoredPropertyName=f"'WeaponIgnored_{mesh_index}'",
                    WeaponShootDataPropertyName=weapon_shoot_datas,
                    **changes)
        print("members:")
        for member in copy:
            print(str(member))
        self.get_turret_weapon_list(turret_index).add(ensure.listrow(copy))