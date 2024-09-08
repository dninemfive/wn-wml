from utils.io import load, write
from message import Message, try_nest
from typing import Self

def path_for(name: str) -> str:
    return f'{name}_cache.txt'

class CacheSet(object):

    def __init__(self: Self, *names: str):
        self.data = {n:{} for n in names}

    def __getitem__(self: Self, key: str) -> dict:
        return self.data[key]

    def load(self: Self, parent_msg: Message | None = None) -> None:
        with try_nest(parent_msg, f'Loading caches') as msg:
            for k in self.data.keys():
                path = path_for(k)
                with msg.nest(path) as _:
                    self.data[k] = load(path_for(k), {})
    
    def save(self: Self, parent_msg: Message | None = None) -> None:
        with try_nest(parent_msg, f'Saving caches') as msg:
            for k in self.data.keys():
                path = path_for(k)
                with msg.nest(path) as _:
                    write(self.data[k], path)