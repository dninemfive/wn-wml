from utils.io import load, write
from message import Message, try_nest
from typing import Self

class Cache(object):
    @property
    def path(self: Self) -> str:
        return f'{self.name}_cache.txt'
    
    def __init__(self: Self, name: str):
        self.name = name
        self.data: dict = {}

    def load(self: Self, msg: Message | None = None) -> None:
        with try_nest(msg, f'Loading {self.path}') as _:
            self.data = load(self.path, {})
    
    def save(self: Self, msg: Message | None = None):
        with try_nest(msg, f'Saving {self.path}') as _:
            write(self.data, self.path)