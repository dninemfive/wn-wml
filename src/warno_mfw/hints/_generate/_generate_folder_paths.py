import os
import shutil
from typing import Iterable

from warno_mfw.utils.types.message import Message, try_nest


def _join(root: str, *paths: str) -> str:
    return os.path.join(root, *paths).replace('\\', '/')

def _make_init(path: str, lines: Iterable[str]) -> None:
        with open(os.path.join(path, '__init__.py'), 'w') as file:
            file.write('\n'.join(lines))

def _ensure_valid_var_name(variable_name: str) -> str:
    if variable_name.startswith(tuple(str(x) for x in range(10))):
        return f'_{variable_name}'
    return variable_name

def is_subfolder(path: str, parent: str) -> bool:
    return path.startswith(parent) or path in parent or path == ''

def _lines_from_folders(rel_path: str, dirs: Iterable[str], filter: str) -> Iterable[str]:
    yielded_any: bool = False
    for dir in dirs:
        # print(dir, filter)
        rel_dir: str = _join(rel_path, dir)
        if is_subfolder(rel_dir, filter):
            # print(rel_dir)
            yield f'from .{dir} import *'
            yielded_any = True
    if yielded_any:
        yield ''

def _lines_from_files(rel_path: str, files: Iterable[str]) -> Iterable[str]:
    for file in files:
        # print(f'{os.path.join(rel_path, file)}')
        variable_name = _ensure_valid_var_name(os.path.splitext(file)[0])
        file_path = _join(rel_path, file)
        yield f"{variable_name}: Literal['{file_path}'] = '{file_path}'"


def generate_module_for_folder(src_path: str, output_path: str, filter: str, msg: Message | None = None) -> None:
    with try_nest(msg, f'generate_module_for_folder({src_path}, {output_path}, {filter})') as msg:
        shutil.rmtree(output_path, ignore_errors=True)
        os.makedirs(output_path, exist_ok=True)
        for subdir, dirs, files in os.walk(src_path):
            rel_path = os.path.relpath(subdir, src_path).replace('\\', '/')
            # with msg.nest(f'rel_path: {rel_path}') as _:
            #     pass
            if not is_subfolder(rel_path, filter):
                continue
            lines: list[str] = []
            result_path = _join(output_path, rel_path)
            os.makedirs(result_path, exist_ok=True)
            with msg.nest(rel_path) as msg2:
                if any(files):
                    lines.append('from typing import Literal\n')
                lines.extend(_lines_from_folders(rel_path, dirs, filter))
                lines.extend(_lines_from_files(rel_path, files))
                _make_init(result_path, lines)
    lines: list[str] = []
    for _, dirs, __ in os.walk(output_path):
        _make_init(output_path, _lines_from_folders('', dirs, ''))
        break