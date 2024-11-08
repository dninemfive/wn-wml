import os
from pathlib import Path
import sys

# fixes ModuleNotFoundError stemming from being run within the module
sys.path[0] = str(Path(sys.path[0]).parent.absolute())

import argparse
import shutil

from warno_mfw.metadata.warno import WarnoMetadata
from warno_mfw.utils import bat
from warno_mfw.utils.types.message import Message
from ndf_parse import Mod
from warno_mfw.hints._generate._generate_folder_paths import generate_module_for_folder

def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generates updated reference information from the WARNO source code. Should be run before working on a mod using dninemfive's WARNO Mod Framework."
    )
    parser.add_argument(['-o', '--output_path'],
                        default='hints',
                        type=str,
                        help="The path the reference information will be created in.")
    parser.add_argument(['-w', '--warno_path'],
                        default=rf"C:\Program Files (x86)\Steam\steamapps\common\WARNO",
                        type=str,
                        help="The path to your WARNO installation.")
    parser.add_argument(['-n', '--mod_name'],
                        default='__TEMP__',
                        type=str,
                        help='The name of the temporary mod which is generated to get the required data.')
    parser.add_argument(['-t', '--test'], action='store_true')
    return parser

def get_mod_path(args: argparse.Namespace) -> str:
    return os.path.join(WarnoMetadata(args['warno_path']).mods_path, args['mod_name'])

def get_output_path(args: argparse.Namespace) -> str:
    result: str = args['output_path']
    if args['test']:
        result = os.path.join(result, '_test')
    return result

parser = make_parser()
args = parser.parse_args()
temp_mod_path = get_mod_path()
output_path = get_output_path()

with Message('Updating reference information for the current WARNO version') as msg:
# generate new mod (named __TEMP__; raise exception if this folder already exists)
    bat.generate_mod(temp_mod_path, msg)
# load mod using ndf-parse
    # mod: Mod
    # with msg.nest('Loading temp mod') as _:
    #     mod = Mod(temp_mod_path, temp_mod_path)
# run code generation
    generate_module_for_folder(temp_mod_path)
# delete __TEMP__ mod
    with msg.nest('Deleting temporary mod') as _:
        shutil.rmtree(temp_mod_path, ignore_errors=True)