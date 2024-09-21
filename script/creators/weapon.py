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
    def __init__(self: Self, ndf: dict[str, List], unit: UnitMetadata, copy_of: str | None = None, parent_msg: Message | None = None, callback: Callable[[str], None] = None):
        self.ndf = ndf
        self.name = ensure.prefix(unit.name, 'WeaponDescriptor_')
        self.copy_of = (ensure.prefix(copy_of, 'WeaponDescriptor_')
                        if copy_of is not None
                        else self.name)
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