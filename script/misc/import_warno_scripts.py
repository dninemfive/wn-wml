from metadata.warno import WarnoMetadata
# https://stackoverflow.com/a/67692
import importlib.util as imp
import os
import sys

def import_script(warno: WarnoMetadata, file_name: str):
    spec = imp.spec_from_file_location(file_name, os.path.join(warno.scripts_path, f'{file_name}.py'))
    result = imp.module_from_spec(spec)
    sys.modules[file_name] = result
    spec.loader.exec_module(result)
    return result