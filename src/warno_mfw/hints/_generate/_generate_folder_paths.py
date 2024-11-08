from dataclasses import dataclass
import os
from typing import Any, Self

def generate_modules_for_folders(root_path: str) -> None:
    generate_module_for_folder(root_path)
    
def generate_module_for_folder(folder_path: str) -> None:
    # generate folder at relative path in _test
    init_file: str = ''
    for subdir, dirs, files in os.walk(folder_path):
        print(subdir)
        for dir in dirs:
            print(f'dir:  {dir}')
        for file in files:
            print(f'file: {file}')
    # import statement for all subfolders
    # if any files:
    #   prepend `from typing import Literal\n`
    #   append a variable definition for every filename like so:
    #       `FileName: Literal['FileName.ndf'] = 'FileName.ndf`
    # write init_file to __init__.py
    # for folder in subfolders, `generate_module_for_folder(path)`