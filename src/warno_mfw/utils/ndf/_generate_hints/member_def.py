from collections import defaultdict
from enum import member
import os
from time import time_ns
from typing import Any, Callable, Iterable, Literal, Self

from ndf_parse import Mod
from ndf_parse.model import ListRow

class MemberDef(object):
    def __init__(self: Self, member_name: str, prefix: str | None = None, is_list_type: bool = False):
        self.member_name = member_name
        self.prefix = prefix
        self.values: set[str] = set()
        self.is_list_type = is_list_type

    def add(self: Self, row: ListRow) -> None:
        if not self.is_list_type:
            self.values.add(strip_prefix_and_quotes(row.value, self.prefix))
        else:
            for item in row.value:
                item: ListRow
                self.values.add(strip_prefix_and_quotes(item.value, self.prefix))

    def enum_line(self: Self) -> str:
        constructor: str = PREFIX if self.prefix is not None else QUOTES
        items = [quote(x) for x in sorted(self.values)]
        if self.prefix is not None:
            items.insert(0, quote(self.prefix))
        return f'{self.member_name.ljust(MEMBER_LEN)}= {constructor}({f',\n{ENUM_INDENT}'.join(items)})'
    
    def literal_line(self: Self) -> str:
        items = [quote(x) for x in sorted(self.values)]
        return f'{self.member_name.ljust(MEMBER_LEN)}= Literal[{f',\n{LITERAL_INDENT}'.join(items)}]'