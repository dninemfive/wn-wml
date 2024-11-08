import os
import shutil
from typing import Iterable, Self

def _make_init(path: str, lines: Iterable[str]) -> None:
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

def make_folder(path: str, must_be_in: str) -> Folder | None:
    pass

def generate_module_for_folder(src_path: str, output_path: str, generated_only: bool) -> None:
    print(output_path)
    shutil.rmtree(output_path, ignore_errors=True)
    os.makedirs(output_path, exist_ok=True)
    _make_init(output_path, ["from .GameData import *"])
    for subdir, dirs, files in os.walk(os.path.join(src_path, 'GameData')):
        rel_path = os.path.relpath(subdir, src_path)
        if generated_only and not (rel_path == 'GameData' or 'Generated' in rel_path):
            continue
        lines: list[str] = []
        result_path = os.path.join(output_path, rel_path)
        os.makedirs(result_path, exist_ok=True)
        print(rel_path)
        if any(files):
            lines.append('from typing import Literal\n')
        for dir in dirs:
            print(f'{os.path.join(rel_path, dir)}')
            lines.append(f'from .{dir} import *')
        if any(dirs):
            lines.append('')
        for file in files:
            # print(f'{os.path.join(rel_path, file)}')
            variable_name = os.path.splitext(file)[0]
            if variable_name.startswith(tuple(str(x) for x in range(10))):
                variable_name = '_' + variable_name
            file_path = os.path.join(rel_path, file).replace('\\', '/')
            lines.append(f"{variable_name}: Literal['{file_path}'] = '{file_path}'")
        _make_init(result_path, lines)