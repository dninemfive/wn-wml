import os
import shutil
    
def _try_mkdir(path: str) -> None:
    try:
        os.mkdir(path)
    except:
        pass

def generate_module_for_folder(src_path: str, output_path: str) -> None:
    print(output_path)
    shutil.rmtree(output_path, ignore_errors=True)
    _try_mkdir(output_path)
    for subdir, dirs, files in os.walk(src_path):
        lines: list[str] = []
        rel_path = os.path.relpath(subdir, src_path)
        result_path = os.path.join(output_path, rel_path)
        _try_mkdir(result_path)
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
            file_path = os.path.join(rel_path, file).replace('\\', '/')
            lines.append(f"{os.path.splitext(file)[0]}: Literal['{file_path}'] = '{file_path}'")
        with open(os.path.join(result_path, '__init__.py'), 'w') as file:
            file.write('\n'.join(lines))