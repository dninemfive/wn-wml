import os
# https://stackoverflow.com/a/1557364
import shutil
# https://stackoverflow.com/a/5469427
from subprocess import PIPE, Popen

from warno_mfw.metadata.mod import ModMetadata
from warno_mfw.metadata.warno import WarnoMetadata
from warno_mfw.utils.types.message import Message, try_nest


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

def reset_source(mod_path: str, mod_name: str, warno_mods_path: str, msg: Message | None = None):
    with try_nest(msg, "Resetting source") as msg2:
        with msg2.nest("Deleting existing files") as _:
            shutil.rmtree(mod_path, ignore_errors=True)
        run_bat(msg, warno_mods_path, "CreateNewMod", mod_name)

def reset_source_for(mod: ModMetadata, msg: Message | None = None):
    reset_source(mod.folder_path, mod.name, mod.warno.mods_path, msg)

def generate_mod(path_or_metadata: str | ModMetadata, msg: Message | None = None):
    path = path_or_metadata.folder_path if isinstance(path_or_metadata, ModMetadata) else path_or_metadata
    run_bat(msg, path, "GenerateMod")