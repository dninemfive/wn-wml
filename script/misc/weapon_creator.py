# right, python is stupid so i can't use type hints for this
# from context.unit_creation_context import UnitCreationContext
from context.module_context import ModuleContext
from message import Message
from metadata.unit import UnitMetadata
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue
from ndf_paths import WEAPON_DESCRIPTOR
from typing import Self
from utils.ndf import edit_members, ndf_path, get_module, replace_unit_module, remove_module

class WeaponCreator(object):
    def __init__(self: Self, ctx, unit: UnitMetadata, copy_of: str):
        self.ctx = ctx
        self.name = f'WeaponDescriptor_{unit.name}'
        self.copy_of = copy_of

    def __enter__(self: Self) -> Self:
        self.root_msg = self.ctx.root_msg.nest(f"Making {self.name}")
        self.root_msg.__enter__()
        with self.root_msg.nest(f"Copying {self.copy_of}") as _:
            self.object = self.make_copy(self.ctx.ndf[WEAPON_DESCRIPTOR])
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        self.apply(self.ctx.ndf, self.root_msg)
        self.root_msg.__exit__(exc_type, exc_value, traceback)

    def apply(self: Self, ndf: dict[str, List], msg: Message):
        with msg.nest(f"Saving {self.new.name}") as msg2:
            self.edit_ammunition(ndf, msg2)

    def make_copy(self: Self, ndf: List) -> Object:
        copy: Object = ndf.by_name(self.src.descriptor_name).value.copy()
        return copy

    @ndf_path(WEAPON_DESCRIPTOR)
    def edit_ammunition(self: Self, ndf: List):
        ndf.add(ListRow(self.object, namespace=self.name, visibility="export"))

    def edit_members(self: Self, **kwargs: CellValue):
        edit_members(self.object, **kwargs)

    def module_context(self: Self, module_type: str) -> ModuleContext:
        return ModuleContext(self.object, module_type)

    def get_module(self: Self, module_type: str) -> Object:
        result: Object | None = get_module(self.object, module_type)
        return result
    
    def remove_module(self: Self, module_type: str) -> None:
        remove_module(self.object, module_type)