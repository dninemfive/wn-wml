from typing import Self

from creators.unit.abc import UnitCreator
from metadata.unit import UnitMetadata

_UnitPair = tuple[UnitMetadata, UnitMetadata | str]

class NewSrcUnitPair(object):
    def __init__(self: Self, new_unit_or_pair: UnitMetadata | UnitCreator | _UnitPair, src_unit: UnitMetadata | str | None = None):
        assert isinstance(new_unit_or_pair, (UnitCreator, _UnitPair)) or src_unit is not None, 'Can only leave src_unit as None if new_unit is UnitCreator!'
        if isinstance(new_unit_or_pair, UnitCreator):
            self.new_unit = new_unit_or_pair.new_unit
            self.src_unit = new_unit_or_pair.src_unit
        elif isinstance(new_unit_or_pair, _UnitPair):
            self.new_unit, self.src_unit = new_unit_or_pair
        else:
            self.new_unit = new_unit_or_pair
        if src_unit is not None:
            self.src_unit = src_unit
        if isinstance(self.src_unit, str):
            self.src_unit = UnitMetadata(self.src_unit)
        assert isinstance(self.new_unit, UnitMetadata)
        assert isinstance(self.src_unit, UnitMetadata)

    def to_tuple(self: Self) -> tuple[UnitMetadata, UnitMetadata]:
        return (self.new_unit, self.src_unit)