from dataclasses import dataclass
from typing import Self
from message import Message
from ndf_parse import Mod
from ndf_parse.model import List, ListRow, Map, MapRow, Object
from ndf_parse.model.abc import CellValue
from utils_ndf import edit_members
from utils_str import max_len
    
@dataclass
class ModMetadata(object):
    author: str
    name: str
    base_path: str
    version: str

    @property
    def source_path(self):
        return f'{self.base_path}{self.name} (input)'
    
    @property
    def output_path(self):
        return f'{self.base_path}{self.name}'