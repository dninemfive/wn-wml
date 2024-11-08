import os
import shutil
from typing import Iterable, Self
from pathlib import Path

from warno_mfw.utils.types.message import Message, try_nest

def _make_init_file(path: str, lines: Iterable[str]) -> None:
        with open(os.path.join(path, '__init__.py'), 'w') as file:
            file.write('\n'.join(lines))

def _ensure_valid_var_name(variable_name: str) -> str:
    if variable_name.startswith(tuple(str(x) for x in range(10))):
        return f'_{variable_name}'
    return variable_name

class Folder(object):
    def __init__(self: Self, path: str):
        self.path = path
        for _, dirs, files in os.walk(path):
            self.dirs = dirs
            self.files = files
            break

    @property
    def init_lines(self: Self) -> Iterable[str]:
        if any(self.files):
            yield 'from typing import Literal\n'
        yield from [f'from {x} import *' for x in self.dirs]
        if any(self.dirs):
            yield ''
        for file in self.files:
            variable_name = _ensure_valid_var_name(os.path.splitext(file)[0])
            file_path = os.path.join(self.path, file).replace('\\', '/')

    def generate(self: Self) -> str | None:
        ...
        # create folder
        # for each folder, call generate
        # write __init__.py

def is_subfolder(path: str, parent: str) -> bool:
    print(f'is_subfolder({path}, {parent})')
    if path == parent:
        return True
    return Path(path) in Path(parent).parents

def make_folder(src_path: str, output_path: str, filter: str, msg: Message | None = None) -> str | None:
    if not is_subfolder(path, filter):
        return None
    os.makedirs(path, exist_ok=True)
    lines: list[str] = []
    folders: list[str] = []
    with try_nest(msg, path) as msg:
        for _, folders, files in os.walk(path):
            if any(files):
                lines.extend('from typing import Literal','')
            for folder in folders:
                if make_folder(folder, filter, msg) is not None:
                    folders.append(folder)
            if any(folders):
                lines.extend([f'from .{x} import *' for x in folders])
                lines.append('')
            for file in files:
                with msg.nest(file) as _:
                    name  = _ensure_valid_var_name(os.path.splitext(file)[0])
                    value = f"'{os.path.join(path, file).replace('\\', '/')}'"
                    lines.append(f"{name}: Literal[{value}] = {value}")
        # _make_init_file(path, lines)
    return path

            


def generate_module_for_folder(src_path: str, output_path: str, generated_only: bool) -> None:
    with Message(f'generate_module_for_folder({src_path}, {output_path}, {generated_only})') as msg:
        shutil.rmtree(output_path, ignore_errors=True)
        make_folder(src_path, output_path, msg)