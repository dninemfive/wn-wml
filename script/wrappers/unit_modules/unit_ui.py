from typing import Self
from wrappers.unit_modules._abc import UnitModuleWrapper
from ndf_parse.model import Object

class UnitUiModuleWrapper(UnitModuleWrapper):
    def __init__(self: Self, ctx, obj: Object):
        self.ctx = ctx
        self.object = obj

    @property
    def UnitRole(self: Self) -> UnitRole: