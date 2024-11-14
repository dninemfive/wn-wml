import os
import sys
from pathlib import Path

# fixes ModuleNotFoundError stemming from being run within the module
module_path = sys.path[0]
sys.path[0] = str(Path(sys.path[0]).parent.absolute())

import argparse
import shutil

from ndf_parse import Mod

from .hints._generate._file_targets import _add_all
from .hints._generate._generate_folder_paths import generate_module_for_folder
from .hints._generate._generate_init import _write
from .metadata.warno import WarnoMetadata
from .utils import bat
from .utils.types.message import Message


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generates updated reference information from the WARNO source code. Should be run before working on a mod using dninemfive's WARNO Mod Framework."
    )
    parser.add_argument('-o', '--output_path',
                        default='hints',
                        type=str,
                        help="The path the reference information will be created in.")
    parser.add_argument('-w', '--warno_path',
                        default=rf"C:\Program Files (x86)\Steam\steamapps\common\WARNO",
                        type=str,
                        help="The path to your WARNO installation.")
    parser.add_argument('-n', '--mod_name',
                        default='__TEMP__',
                        type=str,
                        help='The name of the temporary mod which is generated to get the required data.')
    parser.add_argument('-t', '--test',
                        action='store_true',
                        help="If present, the output will be placed in a _test subfolder.")
    parser.add_argument('-f', '--for_release',
                        action='store_true',
                        help='If specified, will only output the Generated subfolder of GameData. Used to reduce the number of files in official Warno Mod Framework releases.')
    return parser

def get_output_path(args: argparse.Namespace) -> str:
    result: str = args.output_path
    if args.test:
        result = os.path.join(result, '_test')
    return os.path.join(module_path, result)

parser = make_parser()
args = parser.parse_args()
warno = WarnoMetadata(args.warno_path)
temp_mod_path = os.path.join(warno.mods_path, args.mod_name)
output_path = get_output_path(args)

with Message('Updating reference information for the current WARNO version') as msg:
# generate new mod (named __TEMP__; raise exception if this folder already exists)
    try:
        if os.path.exists(temp_mod_path):
            raise Exception(f'Attempted to generate reference information in folder {temp_mod_path}, but this could overwrite an existing mod!')
        bat.reset_source(temp_mod_path, args.mod_name, warno.mods_path, msg)
        with msg.nest('Loading temp mod') as msg2:
            mod = Mod(temp_mod_path, temp_mod_path)
            _add_all(mod, msg2)
            _write(os.path.join(output_path, '__init__.py'))
            
    # run code generation
        generate_module_for_folder(temp_mod_path, os.path.join(output_path, 'paths'), 'GameData/Generated' if args.for_release else 'GameData', msg)
    # delete __TEMP__ mod
    except Exception as e:
        print(f'Failed to generate reference information: {str(e)}')
    finally:
        with msg.nest('Deleting temporary mod') as _:
            shutil.rmtree(temp_mod_path, ignore_errors=True)