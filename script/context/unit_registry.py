from context.mod_creation_context import ModCreationContext
from message import Message
from misc.unit_creator import UnitCreator
from ndf_parse.model import List
from typing import Self

class UnitRegistrar(object):
    @property
    def id_cache(self: Self) -> dict[str, str]:
        return self.ctx.unit_id_cache

    @property
    def ndf(self: Self) -> dict[str, List]:
        return self.ctx.ndf

    def __init__(self: Self, ctx: ModCreationContext, root_msg: Message, initial_id: int):
        self.ctx = ctx
        self.root_msg = root_msg
        self.current_id = initial_id
        
    def create_unit(self: Self, name: str, country: str, copy_of: str) -> UnitCreator:
        return UnitCreator(self, self.ctx.prefix, name, country, copy_of)
    
    def register(self: Self, descriptor_name: str) -> int:
        if descriptor_name not in self.id_cache:            
            self.id_cache[descriptor_name] = self.current_id
            self.current_id += 1
        return self.id_cache[descriptor_name]

    def generate_guid(self: Self, guid_key: str) -> str:
        return self.ctx.generate_guid(guid_key)