from ndf_parse.model import Object
from typing import Self
from utils.ndf import get_module_index

class ModuleContext(object):
    def __init__(self: Self, unit: Object, module_type: str):
        self.unit = unit
        self.module_type = module_type
    
    def __enter__(self: Self) -> Self:
        # self.root_msg = self.ctx.root_msg.nest(f"Editing {self.module_name} on {self.unit.by_member("ClassNameForDebug").value}")
        self.index = get_module_index(self.unit, self.module_type)
        self.object = self.unit.by_member("ModulesDescriptors").value[self.index].value
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        self.unit.by_member("ModulesDescriptors").value[self.index].value = self.object

    