from typing import Self

from warno_mfw.creators.unit.abc import UnitCreator
from warno_mfw.metadata.unit import UnitMetadata

_UnitPair = tuple[UnitMetadata, UnitMetadata | str]

class NewSrcUnitPair(object):
    def __init__(self: Self, new_unit_or_pair: UnitMetadata | UnitCreator | _UnitPair, src_unit: UnitMetadata | str | None = None):
        assert isinstance(new_unit_or_pair, (UnitCreator, tuple)) or src_unit is not None, 'Can only leave src_unit as None if new_unit is UnitCreator!'
        asdf = f'{str(new_unit_or_pair)} {new_unit_or_pair.__class__.__name__} {str(src_unit)} {src_unit.__class__.__name__}'
        if isinstance(new_unit_or_pair, UnitCreator):
            asdf += ' (UnitCreator)'
            self.new_unit = new_unit_or_pair.new_unit
            self.src_unit = new_unit_or_pair.src_unit
        elif isinstance(new_unit_or_pair, tuple):
            asdf += ' (tuple)'
            self.new_unit, self.src_unit = new_unit_or_pair
            if isinstance(self.new_unit, UnitCreator):
                self.new_unit = self.new_unit.new_unit
        else:
            asdf = ' (other)'
            self.new_unit = new_unit_or_pair
        if src_unit is not None:
            self.src_unit = src_unit
        if isinstance(self.src_unit, str):
            self.src_unit = UnitMetadata(self.src_unit)
        assert isinstance(self.new_unit, UnitMetadata), asdf
        assert isinstance(self.src_unit, UnitMetadata)

    def to_tuple(self: Self) -> tuple[UnitMetadata, UnitMetadata]:
        return (self.new_unit, self.src_unit)