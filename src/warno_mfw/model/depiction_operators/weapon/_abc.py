from abc import ABC, abstractmethod
from typing import Self

import warno_mfw.utils.ndf.ensure as ensure
from ndf_parse.model import Object


class WeaponDepictionOperator(ABC):
    def __init__(self: Self, index: int, count: int | None = None, turret_index: int | None = None, anchor_count: int = 1):
        self.index = index
        self.anchors: list[str] = []
        self.count = count if count is not None else anchor_count
        self.turret_index = turret_index if turret_index is not None else index
        for anchor_index in range(anchor_count):
            self.anchors.append(ensure.quoted(f'fx_tourelle{turret_index}_tir_{str(anchor_index).rjust(2, '0')}'))

    @abstractmethod
    def to_ndf(self: Self) -> Object:
        ...