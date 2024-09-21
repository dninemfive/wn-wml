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
    
    @TurretDescriptorList.setter
    def TurretDescriptorList(self: Self, value: list[Object] | List) -> None:
        self.edit_members(TurretDescriptorList=value)

    def get_turret_weapons(self: Self, turret_or_turret_index: Object | ListRow | int) -> List:
        turret: Object = self.TurretDescriptorList[turret_or_turret_index] if isinstance(turret_or_turret_index, int) else ensure.notrow(turret_or_turret_index)
        return turret_or_turret_index.by_member('MountedWeaponDescriptorList').value

    def get_turret_weapon(self: Self, turret_index: int, weapon_index_in_turret: int) -> Object:
        return self.get_turret_weapons(turret_index)[weapon_index_in_turret].value
    
    def get_weapon_counts(self: Self) -> list[list[int]]:
        result = []
        for turret in self.TurretDescriptorList:
            turret_data: list[int] = []
            for weapon in self.get_turret_weapons()
    
    def add_mounted_weapon(self: Self,
                        base: Object | None = None,
                        weapon_index:           int = 0,
                        turret_index:           int = 0,
                        mesh_offset:            int = 1,
                        weapon_shoot_data_ct:   int = 1,
                        **changes) -> None:
        copy: Object = base.copy() if base is not None else self.get_turret_weapon(turret_index, 0)
        mesh_index = weapon_index + mesh_offset
        weapon_shoot_datas = [f'"WeaponShootData_{x}_{mesh_index}"' for x in range(weapon_shoot_data_ct)]
        edit.members(copy,
                    HandheldEquipmentKey=f"'MeshAlternative_{mesh_index}'",
                    SalvoStockIndex=weapon_index,
                    WeaponActiveAndCanShootPropertyName=f"'WeaponActiveAndCanShoot_{mesh_index}'",
                    WeaponIgnoredPropertyName=f"'WeaponIgnored_{mesh_index}'",
                    WeaponShootDataPropertyName=weapon_shoot_datas,
                    **changes)
        self.TurretDescriptorList.add(ListRow(copy))