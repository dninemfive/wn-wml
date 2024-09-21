from typing import Self

from ndf_parse.model import Object
from ndf_parse.model.abc import CellValue
from typing import Self
import utils.ndf.edit as edit
import utils.ndf.unit_module as unit_module

class ModuleContext(object):
    def __init__(self: Self, unit: Object, module_type: str, by_name: bool = False):
        self.unit = unit
        self.module_type = module_type
        self.by_name = by_name
    
    def __enter__(self: Self) -> Self:
        self.index = unit_module.get_index(self.unit, self.module_type, self.by_name)
        self.object: Object = self.unit.by_member("ModulesDescriptors").value[self.index].value
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        self.unit.by_member("ModulesDescriptors").value[self.index].value = self.object

    def edit_members(self: Self, **kwargs: CellValue) -> None:
        edit.members(self.object, **kwargs)

    def remove_member(self: Self, name: str) -> None:
        self.object.remove_by_member(name)