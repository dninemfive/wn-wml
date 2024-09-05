from typing import Self
from ndf_parse import Mod
from ndf_parse.model import List

class NdfEdit(object):
    def __init__(self: Self, path: str, func: callable[List]):
        self.path = path
        self.func = func

    def apply(self: Self, mod: Mod):
        with mod.edit(self.path) as mod:
            self.func(mod)