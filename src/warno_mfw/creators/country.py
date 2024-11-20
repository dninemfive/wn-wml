from __future__ import annotations

from typing import Self

from ndf_parse.model import List, ListRow, Map, MapRow
from ndf_parse.model.abc import CellValue

import warno_mfw.unit_registration.division_unit_registry as ur_dur
import warno_mfw.utils.ndf.edit as edit
from warno_mfw.hints.paths.GameData.Generated import Gameplay
from warno_mfw.metadata.division import DivisionMetadata
from warno_mfw.utils.ndf.decorators import ndf_path
from warno_mfw.utils.types.message import Message

class CountryCreator(object):
    def __init__(self:          Self,
                 key:           str,
                 dico_token:    str):
        self.key = key
        self.dico_token = dico_token

    def apply(self: Self, ndf: dict[str, List], msg: Message):
        pass