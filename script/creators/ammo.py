# right, python is stupid so i can't use type hints for this
# from context.unit_creation_context import UnitCreationContext
from typing import Self

import utils.ndf.edit as edit
import utils.ndf.ensure as ensure
from constants.ndf_paths import AMMUNITION
from context.module_context import ModuleContext
from managers.guid import GuidManager
from metadata.unit import UnitMetadata
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, MemberRow, Object
from ndf_parse.model.abc import CellValue
from utils.ndf.decorators import ndf_path
from utils.ndf.unit_module import get, remove
from utils.types.message import Message, try_nest


class AmmoCreator(object):
    def __init__(self: Self, ndf: dict[str, List], name: str, copy_of: str, guids: GuidManager, parent_msg: Message | None = None):
        self.ndf = ndf
        self.name = ensure.prefix(name, 'Ammo_')
        self.copy_of = ensure.prefix(copy_of, 'Ammo_')
        self.ammo_guid = guids.generate(self.name)
        self.hit_roll_guid = guids.generate(f'{self.name}HitRoll')
        self.parent_msg = parent_msg

    def __enter__(self: Self) -> Self:
        self.msg = try_nest(self.parent_msg, f"Making {self.name}")
        self.msg.__enter__()
        with self.msg.nest(f"Copying {self.copy_of}") as _:
            self.object = self.make_copy(self.ndf[AMMUNITION])
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        self.apply(self.ndf, self.msg)
        self.msg.__exit__(exc_type, exc_value, traceback)

    def apply(self: Self, ndf: dict[str, List], msg: Message):
        with msg.nest(f"Saving {self.name}") as msg2:
            self.edit_ammunition(ndf, msg2)

    def make_copy(self: Self, ndf: List) -> Object:
        copy: Object = ndf.by_name(self.copy_of).value.copy()
        edit.members(copy,
                     DescriptorId=self.ammo_guid)
        # TODO: generic "copy descriptor" method which automatically checks for and sets any member named DescriptorId?
        copy.by_member('HitRollRuleDescriptor').value.by_member('DescriptorId').value = self.hit_roll_guid
        return copy

    # TODO: copy of this but for the missile file?
    @ndf_path(AMMUNITION)
    def edit_ammunition(self: Self, ndf: List):
        ndf.add(ListRow(self.object, namespace=self.name))

    def edit_members(self: Self, **kwargs: CellValue):
        edit.members(self.object, **kwargs)