from context.mod_creation_context import ModCreationContext
from message import Message
from misc.unit_creator import UnitCreator
from ndf_parse.model import List
from typing import Self
from utils.io import load, write

class UnitCreationContext(object):
    @property
    def ndf(self: Self) -> dict[str, List]:
        return self.ctx.ndf

    def __init__(self: Self, ctx: ModCreationContext, root_msg: Message, initial_id: int, id_cache_path: str = "unit_id_cache.txt"):
        self.ctx = ctx
        self.root_msg = root_msg
        self.current_id = initial_id
        self.id_cache_path = id_cache_path
    
    def __enter__(self: Self):
        with self.root_msg.nest("Loading unit ID cache") as _:
            self.id_cache: dict[str, int] = load(self.id_cache_path, {})
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        """
        Closes this context at the end of a `with` block, writing out the cache.
        """
        with self.root_msg.nest("Saving unit ID cache") as _:
            write(self.id_cache, self.id_cache_path)
        self.id_cache = None
    
    def create_unit(self: Self, name: str, copy_of: str):
        return UnitCreator(self, f'{self.ctx.prefix}_{name}', copy_of)
    
    def register(self: Self, descriptor_name: str) -> int:
        if descriptor_name not in self.id_cache:            
            self.id_cache[descriptor_name] = self.current_id
            self.current_id += 1
        return self.id_cache[descriptor_name]

    def generate_guid(self: Self, guid_key: str) -> str:
        return self.ctx.generate_guid(guid_key)