from ndf_parse.model import List, ListRow, Object
import os
import shutil
import utils.ndf
import utils.ndf.ensure as ensure

def add_image(ndf_file: List,
              src_file_path: str,
              mod_output_path: str,
              folder_relative_to_gamedata: str,
              image_name: str,
              texture_bank_name: str,
              image_type: str = 'TUIResourceTexture_Common') -> str:
    texture_obj = make_image_obj(src_file_path,
                                 mod_output_path,
                                 folder_relative_to_gamedata,
                                 image_name,
                                 image_type)
    ndf_file.add(ListRow(texture_obj, namespace=image_name))
    add_texture_to_texture_bank(ndf_file.by_name(texture_bank_name).value, f'"{image_name}"', f'~/{image_name}')
    return f'"{image_name}"'

def add_image_literal(ndf_file: List,
                      src_file_path: str,
                      mod_output_path: str,
                      folder_relative_to_gamedata: str,
                      image_name: str,
                      texture_bank_name: str,
                      image_type: str = 'TUIResourceTexture') -> str:
    texture_obj = make_image_obj(src_file_path,
                                 mod_output_path,
                                 folder_relative_to_gamedata,
                                 image_name,
                                 image_type)
    add_texture_to_texture_bank(ndf_file.by_name(texture_bank_name).value, f'"{image_name}"', texture_obj)
    return f'"{image_name}"'

def copy_image_to_mod_folder(src_file_path: str, mod_output_path: str, folder_relative_to_gamedata: str, image_name: str) -> str:
    destination_folder = os.path.join(mod_output_path, "GameData", folder_relative_to_gamedata)
    os.makedirs(destination_folder, exist_ok=True)
    dst_image_filename = f'{image_name}{os.path.splitext(src_file_path)[1]}'
    result_path = os.path.join(destination_folder, dst_image_filename)
    shutil.copyfile(src_file_path, result_path)
    return gamedata_path(mod_output_path, result_path)

def gamedata_path(mod_output_path: str, path: str) -> str:
    return f'GameData:/{os.path.relpath(path, os.path.join(mod_output_path, 'GameData'))}'

def make_image_obj(src_file_path: str, mod_output_path: str, folder_relative_to_gamedata: str, image_name: str, texture_type: str) -> Object:
    return ensure._object(texture_type,
                          FileName=f'"{copy_image_to_mod_folder(src_file_path, mod_output_path, folder_relative_to_gamedata, image_name)}"')

def add_texture_to_texture_bank(texture_bank: Object, image_key: str, normal_state: Object | str, other_states: dict[str, Object | str] = {}) -> str:
    states: dict[str, Object] = {'~/ComponentState/Normal':normal_state}
    for k, v in other_states:
        states[k] = v
    texture_bank.by_member("Textures").value.add(key=ensure.quoted(image_key), value=ensure._map(states))