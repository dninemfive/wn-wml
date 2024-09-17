from typing import Self
from utils.types.cache import Cache
from utils.types.message import Message, try_nest
import os

class CacheSet(object):

    def __init__(self: Self, base_path: str, *names: str):
        self.base_path = base_path
        self.caches: dict[str, Cache] = {}
        for name in names:
            self.caches[name] = Cache(self.path_for(name))

    def __getitem__(self: Self, name: str) -> Cache:
        return self.caches[name]

    def load(self: Self, parent_msg: Message | None = None) -> None:
        with try_nest(parent_msg, f'Loading caches') as msg:
            for name in self.caches.keys():
                self.caches[name].load(msg)
    
    def save(self: Self, parent_msg: Message | None = None) -> None:
        with try_nest(parent_msg, f'Saving caches') as msg:
            for name in self.caches.keys():
                self.caches[name].save(msg)

    def path_for(self: Self, name: str) -> str:
        return os.path.join(self.base_path, f'{name}.cache')