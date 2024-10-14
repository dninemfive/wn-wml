from abc import ABC, abstractmethod
from typing import Self

import utils.ndf.ensure as ensure
from ndf_parse.model import Object


class WeaponDepictionOperator(ABC):
    def __init__(self: Self, index: int, anchors: list[str] | tuple[int, int]):
        self.index = index
        self.anchors: list[str] = []
        for anchor in anchors:
            if isinstance(anchor, str):
                self.anchors.append(ensure.quoted(anchor))
            else:
                turret_index, shot_count = anchor
                for shot_index in range(shot_count):
                    self.anchors.append(ensure.quoted(f'fx_tourelle{turret_index}_tir_{str(shot_index).rjust(2, '0')}'))

    @property
    def count(self: Self) -> int:
        return len(self.anchors)

    @abstractmethod
    def to_ndf(self: Self) -> Object:
        ...