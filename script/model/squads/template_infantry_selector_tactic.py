from dataclasses import dataclass
from typing import Self
from model.squads._utils import _0

@dataclass
class TemplateInfantrySelectorTactic(object):
    UniqueCount:        int
    surrogate_count:    int

    @staticmethod
    def from_tuple(tuple: tuple[int | str, int | str]) -> Self:
        u, s = tuple
        return TemplateInfantrySelectorTactic(int(u), int(s))

    @property
    def Surrogates(self: Self) -> str:
        return f'TacticDepiction{_0(self.surrogate_count)}_Surrogates'
    
    @property
    def name(self: Self) -> str:
        return f'InfantrySelectorTactic{_0(self.UniqueCount)}{_0(self.surrogate_count)}'
    
    @property
    def tuple(self: Self) -> tuple[int, int]:
        return (self.UniqueCount, self.surrogate_count)