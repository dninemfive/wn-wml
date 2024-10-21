from metadata.mod import ModMetadata
from metadata.warno import WarnoMetadata
# https://stackoverflow.com/a/5469427
from subprocess import PIPE, Popen
from utils.types.message import Message, try_nest
import os
# https://stackoverflow.com/a/1557364
import shutil
import sys

def run_bat(msg: Message | None, folder: str, name: str, *args):
    path = os.path.join(folder, f'{name}.bat')
    # https://stackoverflow.com/a/11729668
    path_and_args = [path, *args, '<nul']
    with try_nest(msg, f"Running `{" ".join(path_and_args)}`\n     in `{folder}`", force_nested=True) as this_msg:
        # https://stackoverflow.com/a/2813530
        process = Popen(path_and_args, cwd=folder, stdout=PIPE)
        while True:
            line = process.stdout.readline()
            if not line:
                break
            print(f'{this_msg.indent_str}  {line.strip().decode()}')
        process.wait()

def reset_source(mod: ModMetadata, warno: WarnoMetadata):
    with Message("Resetting source") as msg:
        with msg.nest("Deleting existing files") as _:
            shutil.rmtree(mod.folder_path, ignore_errors=True)
        run_bat(msg, warno.mods_path, "CreateNewMod", mod.name)

def generate_mod(mod: ModMetadata, msg: Message | None = None):
    run_bat(msg, mod.folder_path, "GenerateMod")