from collections import defaultdict
from enum import member
import os
from time import time_ns
from typing import Any, Callable, Iterable, Literal, Self

from ndf_parse import Mod
from ndf_parse.model import ListRow

from warno_mfw.utils.ndf import ensure

class MemberDef(object):
    def __init__(self: Self, member_name: str, prefix: str | None = None, is_list_type: bool = False):
        self.member_name = member_name
        self.prefix = prefix
        self.values: set[str] = set()
        self.is_list_type = is_list_type

    def add(self: Self, row: ListRow) -> None:
        if not self.is_list_type:
            self.values.add(ensure.no_prefix(ensure.unquoted(row.value), self.prefix))
        else:
            for item in row.value:
                item: ListRow
                self.values.add(ensure.no_prefix(ensure.unquoted(item), self.prefix))