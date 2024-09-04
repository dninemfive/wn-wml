import ndf_parse as ndf
from ndf_parse import Mod
from ndf_parse.model import List
from typing import Self, Generator
from dataclasses import dataclass
from ndf_file_set import NdfFileSet
import ContextManagers as ctx

@dataclass
class UnitNdf(NdfFileSet):
    unite_descriptor: List
    showroom_equivalence: List
    division_packs: List
    deck_serializer: List
    all_units_tactic: List

class MultipleUnitCreationContext(object):
    """ 
    Creates a context for editing all the relevant unit files so they don't have to get closed and reopened over and over 
        See https://ulibos.github.io/ndf-parse/v0.2.0/docs.html#edits
    """
    def __init__(self: Self, context: ctx.ModCreationContext, initial_unit_id: int):
        self.current_unit_id = initial_unit_id

    def __enter__(self: Self):
        self.ndf = UnitNdf(*self.load_files(rf'GameData\Generated\Gameplay',
                                            rf'Gfx\UniteDescriptor',
                                            rf'Gfx\ShowRoomEquivalence',
                                            rf'Decks\DivisionPacks',
                                            rf'Decks\DeckSerializer',
                                            rf'Gfx\AllUnitsTactic'))
        return self
    
    def __exit__(self: Self, exc_type, exc_value, traceback):
        for edit in self.mod.edits:
            self.mod.write_edit(edit)
        self.ndf = None

    def load_files(self: Self, base_path: str, *paths: str) -> Generator[List]:
        for path in paths:
            yield self.mod.edit(f'{base_path}\{path}.ndf').current_tree

    def create_unit(self: Self, unit_name: str, copy_of: str, showroom_equivalent: str | None = None) -> ctx.UnitCreationContext:
        return ctx.UnitCreationContext(self, unit_name, copy_of, showroom_equivalent)