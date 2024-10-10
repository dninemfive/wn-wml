from abc import ABC
from ast import TypeVar
from typing import Self

import utils.ndf.edit as edit
from ndf_parse.model import Object
from ndf_parse.model.abc import CellValue

UnitModuleKey = tuple[str, str | None]


class UnitModuleWrapper(ABC):
    _module_key: UnitModuleKey = None