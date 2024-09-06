from ndf_parse.model import List, Object
from typing import Self

class UnitWrapper(object):
    def __init__(self: Self, obj: Object):
        self.obj = obj

    @property
    def descriptor_id(self: Self) -> str:
        return self.obj.by_member("DescriptorId").value
    
    @descriptor_id.setter
    def descriptor_id(self: Self, val: str):
        self.obj.by_member("DescriptorId").value = val

    @property
    def class_name_for_debug(self: Self) -> str:
        return self.obj.by_member("ClassNameForDebug").value.strip("'")
    
    @class_name_for_debug.setter
    def class_name_for_debug(self: Self, val: str):
        self.obj.by_member("ClassNameForDebug").value = f"'{val}'"

    @property
    def modules_descriptors(self: Self) -> List:
        return self.obj.by_member("ModulesDescriptors").value
    
    def __getitem__(self: Self, type: str):
        """ TODO """
        pass