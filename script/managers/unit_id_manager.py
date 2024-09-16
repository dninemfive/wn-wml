from context.mod_creation_context import ModCreationContext
from misc.unit_creator import UnitCreator
from typing import Self

class UnitIdManager(object):
    @property
    def id_cache(self: Self) -> dict[str, str]:
        return self.ctx.unit_id_cache

    def __init__(self: Self, ctx: ModCreationContext, initial_id: int):
        self.ctx = ctx
        self.current_id = initial_id
        
    def create_unit(self: Self, name: str, country: str, copy_of: str) -> UnitCreator:
        return UnitCreator(self, self.ctx.prefix, name, country, copy_of)
    
    def register(self: Self, descriptor_name: str) -> int:
        if descriptor_name not in self.id_cache:            
            self.id_cache[descriptor_name] = self.current_id
            self.current_id += 1
        return self.id_cache[descriptor_name]