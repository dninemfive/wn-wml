import argparse
import os
import shutil

from warno_mfw.metadata.warno import WarnoMetadata
from warno_mfw.utils import bat
from warno_mfw.utils.types.message import Message
from ndf_parse import Mod


parser = argparse.ArgumentParser(
    description="Generates updated reference information from the WARNO source code. Should be run before working on a mod using dninemfive's WARNO Mod Framework."
)
parser.add_argument(['-o', '--output_path'],
                    default='utils/ndf/_test',
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
args = parser.parse_args()
temp_mod_path = os.path.join(WarnoMetadata(args['warno_path']).mods_path, args['mod_name'])
with Message('Updating reference information for the current WARNO version') as msg:
# generate new mod (named __TEMP__; raise exception if this folder already exists)
    bat.generate_mod(temp_mod_path, msg)
# load mod using ndf-parse
    mod: Mod
    with msg.nest('Loading temp mod') as _:
        mod = Mod(temp_mod_path, temp_mod_path)
# run code generation
# delete __TEMP__ mod
    with msg.nest('Deleting temporary mod') as _:
        shutil.rmtree(temp_mod_path, ignore_errors=True)