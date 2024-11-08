import os
from typing import Callable
from ndf_parse import Mod
from ndf_parse.model import ListRow, Object

from ._member_def import MemberDef
from ._member_targets import TARGETS

MemberDefFormatter = Callable[[MemberDef], str]

def add(item: ListRow, targets: dict[str, MemberDef]) -> str:
    for module_row in item.value.by_member('ModulesDescriptors').value:
        module = module_row.value
        if isinstance(module, Object) and module.type in targets:
            for member_def in targets[module.type]:
                member_def.add(module.by_member(member_def.member_name))

def write(folder: str, name: str, formatter: MemberDefFormatter) -> str:
    with open(os.path.join(folder, f'{name}.py'), 'w') as file:
        file.write('\n\n'.join(tolines(formatter)))
    return f'from .{name} import *'

def generate(mod: Mod) -> None:
    for file_path, file_targets in TARGETS.items():
        with mod.edit(file_path) as file:
            for item in file:
                add(item, file_targets)